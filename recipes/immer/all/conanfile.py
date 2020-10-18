#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration

class ImmerConan(ConanFile):
    name = "immer"
    homepage = "https://github.com/arximboldi/immer"
    url = "https://github.com/conan-io/conan-center-index"
    description = "Postmodern immutable and persistent data structures for C++"
    topics = ("cpp14", "cpp17", "immutable", "containers", "data-structures")
    license = "BSL-1.0"
    no_copy_source = True
    settings = "compiler"

    _source_subfolder = "source_subfolder"

    def _validate_compiler_settings(self):
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, "14")
        minimum_version = {
            "clang": 3.8,
            "apple-clang": 10,
            "gcc": 6,
            "Visual Studio": 14.0,
        }.get(str(self.settings.compiler))
        if not minimum_version:
            self.output.warn("Unknown compiler: assuming compiler supports C++14")
        elif tools.Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration("Compiler does not support C++14")

    def configure(self):
         self._validate_compiler_settings()

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("immer-{}".format(self.version), self._source_subfolder)

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*", dst=os.path.join("include", "immer"), src=os.path.join(self._source_subfolder, "immer"))

    def package_id(self):
        self.info.header_only()
