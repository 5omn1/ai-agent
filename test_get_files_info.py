from functions.get_files_info import get_files_info


def main():
    print("Result for current directory:")
    result = get_files_info("calculator", ".")
    for line in result.splitlines():
        print(f"  {line}")

    print("\nResult for 'pkg' directory:")
    result = get_files_info("calculator", "pkg")
    for line in result.splitlines():
        print(f"  {line}")

    print("\nResult for '/bin' direcotry:")
    result = get_files_info("calculator", "/bin")
    for line in result.splitlines():
        print(f"  {line}")

    print("\nResult for '../' directory:")
    resutl = get_files_info("calculator", "../")
    for line in resutl.splitlines():
        print(f"  {line}")


if __name__ == "__main__":
    main()
