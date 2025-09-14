def string_find(input_0_0, input_0_1):
    a = str(input_0_0)
    b = str(input_0_1)

    if a == "":
        return -1
    if b == "":
        return -1

    if len(b) > len(a):
        return -2
    if len(b) == len(a):
        if a == b:
            return 10
        return 11

    if a.startswith(b):
        return 20
    if a.endswith(b):
        return 21
    if b in a:
        idx = a.find(b)
        if idx < len(a) // 2:
            return 22
        return 23

    return -3
