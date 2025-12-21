import lldb
from datetime import datetime, timezone

def underlying_type(type_ref: lldb.SBType) -> lldb.SBType:
    return type_ref.GetDereferencedType() if type_ref.IsReferenceType() else type_ref


class BoostOptional:
    def __init__(self, valobj: lldb.SBValue, dict):
        self.valobj = valobj

    def num_children(self):
        return 1

    def has_children(self):
        return True

    def get_child_index(self, name):
        return None

    def get_child_at_index(self, index):
        is_initialized = self.valobj.GetChildMemberWithName("m_initialized").GetValueAsUnsigned() == 1

        if not is_initialized:
            return self.valobj.CreateValueFromExpression("val", '(const char*)"none"')

        return self.valobj.GetChildMemberWithName("m_storage").CreateChildAtOffset(
            "val", 0, underlying_type(self.valobj.GetType()).GetTemplateArgumentType(0)
        )

    def update(self):
        pass


def BoostDate(valobj: lldb.SBValue, dict):
    days = valobj.GetChildMemberWithName('days_').GetValueAsUnsigned()

    if days == 4294967294:  # 2**32 - 2
        return "not-a-date"
    elif days == 0:
        return "-inf"
    elif days == 4294967295:  # 2**32 - 1
        return "+inf"

    a = days + 32044
    b = (4 * a + 3) // 146097
    c = a - ((146097 * b) // 4)
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - ((153 * m + 2) // 5) + 1
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + (m // 10)

    if year < 0:
        return f"not-a-date: days={days}"

    return f"{year}-{month:02}-{day:02}"


def BoostPtime(valobj: lldb.SBValue, dict):
    time_count = valobj.GetChildMemberWithName('time_').GetChildMemberWithName('time_count_').GetChildMemberWithName('value_').GetValueAsUnsigned()

    if time_count == 9223372036854775806:  # 2**64/2 - 2
        return "not-a-date-time"
    elif time_count == 9223372036854775808:  # 2**64/2
        return "-inf"
    elif time_count == 9223372036854775807:  # 2**64/2 - 1
        return "+inf"

    epoch = 210866803200 # 1970-01-01
    try:
        dt = datetime.fromtimestamp(time_count // 1000000 - epoch, timezone.utc)
        return f"{dt.strftime("%Y-%m-%d %H:%M:%S")}"
    except Exception as e:
        return f"not-a-date-time: {str(e)}"


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('type synthetic add -l boost_formatter.BoostOptional -x "^boost::optional<.+>$"')
    debugger.HandleCommand('type summary add -F boost_formatter.BoostDate "boost::gregorian::date"')
    debugger.HandleCommand('type summary add -F boost_formatter.BoostPtime "boost::posix_time::ptime"')
