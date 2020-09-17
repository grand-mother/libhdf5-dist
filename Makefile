CFLAGS= -Iinclude
LDFLAGS= -Llib -lhdf5
ifeq ($(shell uname -s),Linux)
LDFLAGS+= '-Wl,-rpath,$$ORIGIN/../lib'
endif

bin/example: src/example.c
	@mkdir -p bin
	$(CC) -o $@ $(CFLAGS) $^ $(LDFLAGS)

.PHONY: clean distclean
clean:
	rm -rf bin

distclean: | clean
	rm -rf lib include libhdf5-*.tgz
