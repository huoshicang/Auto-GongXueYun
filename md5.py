from hashlib import md5


def Md5(text: str):
    print("    md5加密", end="    ")
    s = text + "3478cbbc33f84bd00d75d7dfa69e0daa"
    return md5(s.encode("utf-8")).hexdigest()
