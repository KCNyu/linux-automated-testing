#!/usr/bin/perl

# Function declarations for parser
sub process_line;
sub process_testdir;
sub process_sub_test_name;
sub filter_test_name;
sub process_test;
sub process_result;
sub print_result;

# Function declarations for LAVA
sub check_lava;
sub analyze_result;

my ( $line, $content, $testdir );
my @sub_test_array = ();
my $id_counter     = 0;
my $results        = [];
my $lava_status    = 0;

sub print_help {
    print <<"END_HELP";
Usage: perl parse.pl [OPTIONS]

Options:
  -h, --help        Show this help message
  -i, --input FILE  Specify input file
  -j, --save-json   Save results in JSON format
  -c, --save-csv    Save results in CSV format
END_HELP
}

sub parse {

    my ($filename) = @_;

    open( my $file, "<", $filename ) or die "Can't open $filename: $!\n";

    while ( $line = <$file> ) {
        $content .= $line;
        ( $content, $testdir ) =
          process_line( $line, $content, $testdir, \@sub_test_array );
    }

    close($file);
}

sub process_line {
    my ( $line, $content, $testdir, $sub_test_array ) = @_;
    my $reason = "";

    if ( $line =~ m|^# selftests: (.*)$| ) {
        $testdir = process_testdir($1);
    }
    elsif ( $line =~ m|^(?:# )*(not )?ok (\d+) ([^#]+)(# (SKIP)?)?| ) {
        my ( $not, $number, $test, $skip ) = ( $1, $2, $3, $5 );
        $test = process_test( $test, $testdir, $number );
        my $result = process_result( $not, $skip );
        if ( $result eq "fail" or $result eq "skip" ) {
            if ( $content =~ /(TAP version.*)/s ) {
                $reason = $1;
            }
            else {
                $reason = $content;
            }
            if (@sub_test_array) {
                $reason .= "\n# The following sub-tests did not succeed\n";
                foreach my $sub_test (@sub_test_array) {
                    $reason .= "# " . $sub_test . "\n";
                }
                @sub_test_array = ();
            }

        }
        print_result( $result, $test, $reason );
        if ( index( $test, "1.global_main_test" ) eq -1 ) {
            $content = "";
        }
    }
    elsif (
           $line =~ m/^#\s*\[\d+\]\s+.*?\[(PASS|UNSUPPORTED|FAIL|UNRESOLVED)\]$/
        || $line =~ m/^#\s+\[(PASS|UNSUPPORTED|FAIL|UNRESOLVED)\]$/ )
    {
        my $result = lc($1);
        my $test   = process_sub_test_name( $line, $testdir, $content );

        if ( $result ne "pass" ) {
            if ( $content =~ /(TAP version.*)/s ) {
                $reason = $1;
            }
            else {
                $reason = $content;
            }
            push @sub_test_array, $test;
        }

        $content = "";
        print_result( $result, $test, $reason );
    }

    return ( $content, $testdir, $sub_test_array );
}

sub process_testdir {
    my ($testdir) = @_;
    $testdir =~ s|[:/]\s*|.|g;
    return $testdir;
}

sub process_sub_test_name {
    my ( $line, $testdir, $content ) = @_;
    my ( $number, $filtered_test );

    my $test = $testdir;

    if ( $line =~ m|#\s*\[(\d+)\]\s*(.*)\s*\[.*\]| ) {
        $number        = $1;
        $filtered_test = filter_test_name($2);
        $filtered_test =~ s/_$//;
        $test = "$testdir.$number.$filtered_test";
    }
    elsif ( $content =~ m/running\s+(.+)/ ) {
        my $maybe_test_name = filter_test_name($1);
        $test = "$testdir.$maybe_test_name";
    }
    return $test;
}

sub filter_test_name {
    my ($test) = @_;

    # Remove spaces around non-alphanum characters
    $test =~ s|\s*([^a-zA-Z0-9])\s*|$1|g;

    # Replace all non-alphanumeric characters with underscores
    $test =~ s|[^a-zA-Z0-9]|_|g;

    # Collapse multiple underscores to a single underscore
    $test =~ s|__+|_|g;

    # Remove leading hyphens (and spaces before them, if any)
    $test =~ s|^\s*-||;

    # Remove leading undersocres
    $test =~ s|^_+||;

    # Remove ending underscores
    $test =~ s|_+$||;

    return $test;
}

sub process_test {
    my ( $test, $testdir, $number ) = @_;
    $test =~ s|\s+$||;
    if ( $test =~ /selftests: (.*)/ ) {
        $test = process_testdir($1);
    }
    else {
        $test = filter_test_name($test);
        $test = "$testdir.$number.$test";
    }
    return $test;
}

sub process_result {
    my ( $not, $skip ) = @_;
    my $result;
    if ( $skip eq "SKIP" ) {
        $result = "skip";
    }
    elsif ( $not eq "not " ) {
        $result = "fail";
    }
    else {
        $result = "pass";
    }
    return $result;
}

sub check_lava {
    my $command = "command -v lava-test-case >/dev/null 2>&1";
    $lava_status = system($command);
}

sub print_result {
    my ( $result, $test, $reason ) = @_;

    my %result_hash = (
        "id"     => $id_counter++,
        "test"   => $test,
        "result" => $result,
        "reason" => $reason
    );

    # Return early if $test contains "1.global_main_test"
    return if index( $test, "1.global_main_test" ) != -1;

    push @$results, \%result_hash;
}

sub make_unique {
    my %namecounts;
    for my $r (@$results) {
        my $name = $r->{"test"};
        $namecounts{$name} =
          ( exists $namecounts{$name} ? $namecounts{$name} : 0 ) + 1;
        if ( $namecounts{$name} > 1 ) {
            $r->{"test"} .= "_dup$namecounts{$name}";
        }
    }
}

sub analyze_result {
    make_unique();

    my $pre_name = @$results[0]->{"test"};
    $pre_name =~ s/=[[:digit:]]//;

    my $pre_category = ( split /\./, $pre_name )[0];

    if ( $lava_status eq 0 ) {
        my $command = "lava-test-set start $pre_category";
        system($command);
    }
    else {
        my $command = "echo \"<LAVA_SIGNAL_TESTSET START $pre_category>\"";
        system($command);
    }

    foreach my $res (@$results) {
        my $test   = $res->{"test"};
        my $result = $res->{"result"};
        my $reason = $res->{"reason"};

        $test =~ s/=[[:digit:]]//;
        chomp($reason);

        my $category = ( split /\./, $test )[0];
        if ( $category ne $pre_category ) {
            if ( $lava_status eq 0 ) {
                my $command = "lava-test-set stop $pre_category";
                system($command);

                $command = "lava-test-set start $category";
                system($command);

                $pre_category = $category;
            }
            else {
                my $command =
                  "echo \"<LAVA_SIGNAL_TESTSET STOP $pre_category>\"";
                system($command);

                $command = "echo \"<LAVA_SIGNAL_TESTSET START $category>\"";
                system($command);

                $pre_category = $category;
            }
        }

        if ( $lava_status eq 0 ) {
            if ( $result eq "pass" ) {
                my $command = "lava-test-case $test --result $result";
                system($command);
            }
            elsif ($result eq "skip"
                || $result eq "unresolved"
                || $result eq "unsupported" )
            {
                my $command = "lava-test-case $test --result \"skip\"";
                system($command);
            }
            elsif ( $result eq "fail" ) {

                # my $print_reason_command = "echo \"$reason\"";
                my $print_reason_command =
                  "lava-test-case $test --shell echo \"$reason\"";
                system($print_reason_command);

                my $command = "lava-test-case $test --result \"fail\"";
                system($command);
            }
        }
        else {
            if ( $result eq "pass" ) {
                my $output  = "<TEST_CASE_ID=${test} RESULT=${result}>";
                my $command = "echo \"\033[0;32m$output\033[0m\"";
                system($command);
            }
            elsif ($result eq "skip"
                || $result eq "unresolved"
                || $result eq "unsupported" )
            {
                my $print_reason_command = "echo \"\033[0;33m$reason\033[0m\"";
                system($print_reason_command);

                my $output  = "<TEST_CASE_ID=${test} RESULT=${result}>";
                my $command = "echo \"\033[0;36m$output\033[0m\"";
                system($command);
            }
            elsif ( $result eq "fail" ) {
                my $print_reason_command = "echo \"\033[0;33m$reason\033[0m\"";
                system($print_reason_command);

                my $output  = "<TEST_CASE_ID=${test} RESULT=fail>";
                my $command = "echo \"\033[0;31m$output\033[0m\"";
                system($command);
            }
        }
    }

    if ( $lava_status eq 0 ) {
        my $command = "lava-test-set stop $pre_category";
        system($command);
    }
    else {
        my $command = "echo \"<LAVA_SIGNAL_TESTSET STOP $pre_category>\"";
        system($command);
    }
}

sub escape_json_string {
    my ($str) = @_;
    $str =~ s/\\/\\\\/g;
    $str =~ s/"/\\"/g;
    $str =~ s/\n/\\n/g;
    $str =~ s/\r/\\r/g;
    $str =~ s/\t/\\t/g;
    return $str;
}

sub save_results_to_json {
    my ($results) = @_;

    my $filename = "results.json";
    open( my $fh, '>', $filename )
      or die "Could not open file '$filename' $!";

    print $fh "[\n";

    my $first_item = 1;
    foreach my $item (@$results) {
        print $fh "," unless $first_item;
        $first_item = 0;

        my @pairs;
        foreach my $key ( keys %$item ) {
            my $value = $item->{$key};

            if ( $value =~ /^\d+$/ ) {
                push @pairs,
                  sprintf( '"%s":%s', escape_json_string($key), $value );
            }
            else {
                push @pairs,
                  sprintf( '"%s":"%s"',
                    escape_json_string($key),
                    escape_json_string($value) );
            }
        }

        print $fh "    {" . join( ", ", @pairs ) . "}\n";
    }

    print $fh "]\n";

    close $fh;
    print "Results saved to JSON file'$filename'.\n";
}

sub save_results_to_csv {
    my ($results) = @_;

    my $filename = "results.csv";

    open( my $fh, '>', $filename ) or die "Could not open file '$filename' $!";

    my @headers = qw(test result);

    # print $fh join(",", @headers) . "\n";

    foreach my $item (@$results) {
        my $name   = $item->{test};
        my $result = $item->{result};

        print $fh "$name $result\n";
    }

    close $fh;
    print "Results saved to CSV file '$filename'.\n";
}

# ==============================================================================

sub main() {
    if ( scalar(@ARGV) == 0 ) {
        print_help();
        exit;
    }
    my $input_file = '';
    my $save_json  = 0;
    my $save_csv   = 0;
    for ( my $i = 0 ; $i <= $#ARGV ; $i++ ) {
        my $arg = $ARGV[$i];
        if ( $arg eq '-h' || $arg eq '--help' ) {
            print_help();
            exit;
        }
        elsif ( $arg eq '-i' ) {
            $i++;
            $input_file = $ARGV[$i] if defined $ARGV[$i];
        }
        elsif ( $arg =~ /^--input=(.+)$/ ) {
            $input_file = $1;
        }
        elsif ( $arg eq '-j' || $arg eq '--save-json' ) {
            $save_json = 1;
        }
        elsif ( $arg eq '-c' || $arg eq '--save-csv' ) {
            $save_csv = 1;
        }
    }

    die "An input file is required. Use -i or --input option.\n"
      unless $input_file;
    check_lava();
    parse($input_file);
    analyze_result();

    if ($save_json) {
        save_results_to_json($results);
    }
    if ($save_csv) {
        save_results_to_csv($results);
    }
}

main();
