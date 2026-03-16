import lldb

def QuantLibDate(valobj: lldb.SBValue, dict):
    date_number = valobj.GetChildMemberWithName('serialNumber_').GetValueAsUnsigned()
    serial_number = 32044 + date_number + 1721060+693960-1

    i = (146097*((4*serial_number+3)//146097))//4
    k = 1461*((4*(serial_number-i)+3)//1461)
    n = (5*(serial_number-i-k//4)+2)//153

    y = 100*((4*serial_number+3)//146097)+((4*(serial_number-i)+3)//1461)-4800+(n//10)
    m = n+3-12*(n//10)
    d = (serial_number-i-k//4)-((153*n+2)//5)+1

    return f'{y:04}-{m:02}-{d:02}'


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('type summary add -F quantlib_formatter.QuantLibDate "QuantLib::Date"')
