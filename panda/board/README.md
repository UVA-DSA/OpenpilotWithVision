Dependencies
--------

**Mac**

```
./get_sdk_mac.sh
```

**Debian / Ubuntu**

```
./get_sdk.sh
```


Programming
----

**Panda**

```
make
```

**NEO**

```
make -f Makefile.legacy
```

Troubleshooting
----

If your panda will not flash and is quickly blinking a single Green LED, use:
```
make recover
```


[dfu-util](http://github.com/dsigma/dfu-util.git) for flashing
