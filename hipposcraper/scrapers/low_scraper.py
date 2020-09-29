#!/usr/bin/env python3
"""Module for LowScraper"""
import json
import re
import sys

_PUTCHAR = """#include <unistd.h>

/**
 * _putchar - write a character to stdout
 * @c: the character to write
 *
 * Return: On error, -1 is returned, and errno is set appropriately.
 * Otherwise, 1 is returned.
 */
int _putchar(char c)
{
\treturn (write(STDOUT_FILENO, &c, 1));
}"""


class LowScraper:
    """LowParse class

    Low-Level_Programming project scraper.

    Args:
        soup (obj): BeautifulSoup obj containing parsed link

    Attributes:
        header_check (int): if 0, there is header. if 1, there is no header
    """
    header_check = 0

    def __init__(self, soup):
        """Instantiation of LowScraper"""
        self.soup = soup
        self.putchar_check = self.find_putchar()
        self.prototypes_list = self.find_prototypes()
        self.header_name = self.find_header()
        self.file_names = self.find_files()

    def find_putchar(self):
        """Method to check for holberton's `_putchar`"""
        match = self.soup.find(string=re.compile("You are allowed to use"))
        try:
            if len(match) == 23:
                return match.next_sibling.text
        except TypeError:
            return None

    def write_putchar(self):
        """Method to create Holberton's `_putchar` if required"""
        if self.putchar_check == "_putchar":
            print("  -> Creating _putchar.c ...")
            try:
                with open("_putchar.c", "w") as ostream:
                    print(_PUTCHAR, file=ostream)
            except OSError:
                print("     [ERROR] Failed to write _putchar")
            else:
                print("     Done.")

    def find_prototypes(self):
        """Method to scrape for C prototypes"""
        temp = []
        find_protos = self.soup.find_all(string=re.compile("Prototype: "))
        for item in find_protos:
            temp.append(item.next_sibling.text.replace(";", ""))
        return temp

    def find_header(self):
        """Method to scrape for C header file name"""
        try:
            finder = "forget to push your header file"
            header_text = self.soup.find(string=re.compile(finder)).previous_element
            return header_text.previous_element.previous_element
        except AttributeError:
            self.header_check = 1
            return ""

    def write_header(self):
        """Method to write/create C header file if required"""
        if self.header_check == 0:
            # Making header include guard string
            include_guard = self.header_name
            include_guard = include_guard.replace('.', '_', 1)
            include_guard = include_guard.upper()

            print("  -> Creating header file...")
            try:
                w_header = open(self.header_name, "w+")
                w_header.write('#ifndef %s\n' % include_guard)
                w_header.write('#define %s\n' % include_guard)
                w_header.write("\n")
                w_header.write("#include <stdio.h>\n")
                w_header.write("#include <stdlib.h>\n")
                w_header.write("\n")

                try:
                    if self.putchar_check == "_putchar":
                        w_header.write("int _putchar(char c);\n")
                except TypeError:
                    pass

                n = 0
                for item in self.prototypes_list:
                    if n == len(self.prototypes_list):
                        break
                    w_header.write(self.prototypes_list[n] + ";\n")
                    n += 1

                w_header.write("\n")
                w_header.write('#endif /* %s */' % include_guard)
                w_header.close()
                print("     Done.")
            except AttributeError:
                print("     [ERROR] Failed to create header file.")
        else:
            pass

    def find_files(self):
        """Method to scrape for C file names"""
        return self.soup.find_all(string=re.compile("File: "))

    def write_files(self):
        """Method to write/create C files

        Handles multiple file names by searching for ','.
        """
        self.write_putchar()
        self.write_header()
        i = 0
        print("  -> Creating task files...")
        for item in self.file_names:
            file_text = item.next_sibling.text
            # Breaks incase more function names over file names
            if self.prototypes_list != 0:
                if (i == len(self.prototypes_list)):
                    break

            try:
                # Pulling out name of function for documentation
                if self.prototypes_list != 0:
                    func_name = self.prototypes_list[i]
                    func_name = func_name.split("(", 1)[0]
                    tmp_split = func_name.split(" ")
                    func_name = tmp_split[len(tmp_split) - 1]
                    tmp_split = func_name.split("*")
                    func_name = tmp_split[len(tmp_split) - 1]

                # Removing string after first comma (multiple file names)
                find_comma = file_text.find(",")
                if find_comma != -1:
                    w_file_name = open(file_text[:find_comma], "w+")
                else:
                    w_file_name = open(file_text, "w+")

                if self.header_check != 1:
                    w_file_name.write('#include "%s"\n\n' % self.header_name)
                    w_file_name.write("/**\n")
                    w_file_name.write(" * %s -\n" % func_name)
                    w_file_name.write(" *\n")
                    w_file_name.write(" * Return: \n")
                    w_file_name.write(" */\n")
                    w_file_name.write("%s\n" % self.prototypes_list[i])
                    w_file_name.write("{\n")
                    w_file_name.write("\n")
                    w_file_name.write("}")
                    w_file_name.close()
                i += 1
            except (AttributeError, IndexError):
                print("     [ERROR] Failed to create task file {}".format(
                    file_text
                ))
                continue
        print("     Done.")

    def write_checker(self):
        with open("check.sh", "w") as f:
            f.write("#!/usr/bin/env bash\n")
            f.write("betty ")
            if self.header_name:
                f.write('"%s" ' % self.header_name)
            if self.file_names:
                for i in self.file_names:
                    f.write('"%s" ' % i.next_sibling.text)
