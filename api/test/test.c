#include <sys/mman.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// #include "kselftest_harness.h"
#include "../../api/kselftest_harness.h"

FIXTURE(t1)
{
	int fd;
	unsigned int page_size;
	unsigned int page_shift;
};

FIXTURE(t2)
{
	int fd;
	int fd2;
	unsigned int page_size;
	unsigned int page_shift;
};

FIXTURE_SETUP(t1)
{
	self->fd = 1;
	self->page_size = 2;
	self->page_size = 3;
}

FIXTURE_SETUP(t2)
{
	self->fd = 4;
	self->fd2 = 5;
	self->page_size = 6;
	self->page_size = 7;
}

FIXTURE_TEARDOWN(t1)
{
	ASSERT_EQ(0, 0);
	self->fd = -1;
}

FIXTURE_TEARDOWN(t2)
{
	TH_LOG("dsaldjsal");
	// ASSERT_EQ(0, 0);
	self->fd = -1;

	// ASSERT_EQ(0, 0);
	self->fd2 = -1;
}

TEST_F(t2, open_close_2)
{
	ASSERT_NE(self->fd, 4)
	{
		TH_LOG("Error: couldn't map the space we need for the test\n");
		exit(1);
	}

	EXPECT_EQ(self->fd, 2);
}

TEST(hello)
{
	ASSERT_EQ(1, 1);
}

TEST_F(t1, open_closed)
{
	ASSERT_EQ(self->fd, 1);
}
TEST_F(t1, open_closed_2)
{
	ASSERT_EQ(self->fd, 1);
}
TEST(main_test)
{
	ASSERT_EQ(1, 2)
	{
		TH_LOG("Error: couldn't map the space we need for the test\n");
	}
}

TEST_HARNESS_METADATA_MAIN("vm", "hello", NORMAL)