# lldb-formatters

The LLDB formatter for boost and quantlib classes:
* `boost::optional`
* `boost::gregorian::date`
* `boost::posix_time::ptime`
* `QuantLib::Date`


Make `~/.lldbinit` with the following command to configure the formatters for `lldb`.
```
command script import <path to formatters>/boost_formatter.py
command script import <path to formatters>/quantlib_formatter.py

```

For using the formatters with extension `CodeLLDB` in Visual Studio Code the following line should be added to `settings.json`
```
    "lldb.launch.initCommands": [
        "command source ${env:HOME}/.lldbinit"
    ],
```
