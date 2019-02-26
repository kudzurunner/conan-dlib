from conans import ConanFile, CMake, tools
import os


class DlibConan(ConanFile):
    name = "dlib"
    version = "19.16"
    license = "http://dlib.net/license.html"
    author = "KudzuRunner"
    url = "https://github.com/kudzurunner/conan-dlib"
    description = "Dlib is a modern C++ toolkit containing machine learning algorithms and tools"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "with_jpeg": [True, False],
        "with_png": [True, False],
        "with_gif": [True, False],
        "with_lapack": [True, False],
        "with_blas": [True, False],
        "with_sqlite3": [True, False],
        "with_cuda": [True, False],
        "disable_gui": [True, False],
        "enable_iso_cpp_only": [True, False],
        "enable_stack_trace": [True, False],
        "enable_assets": [True, False],
        "enable_sse2": [True, False],
        "enable_sse4": [True, False],
        "enable_avx": [True, False]
    }
    default_options = {
        "shared": False,
        "with_jpeg": True,
        "with_png": True,
        "with_gif": True,
        "with_lapack": True,
        "with_blas": True,
        "with_sqlite3": True,
        "with_cuda": True,
        "disable_gui": True,
        "enable_iso_cpp_only": False,
        "enable_stack_trace": False,
        "enable_assets": False,
        "enable_sse2": True,
        "enable_sse4": True,
        "enable_avx": True
    }
    generators = "cmake"
    source_name = "{}-{}".format(name, version)
    install_name = "install"

    def requirements(self):
        if not self.options.enable_iso_cpp_only:
            if self.options.with_jpeg:
                self.requires.add('libjpeg-turbo/2.0.1@kudzurunner/stable')
            if self.options.with_png:
                self.requires.add('libpng/1.6.36@bincrafters/stable')
            if self.options.with_gif:
                self.requires.add('giflib/5.1.4@bincrafters/stable')
            if self.options.with_sqlite3:
                self.requires.add('sqlite3/3.27.2@bincrafters/stable')
            if self.options.with_lapack or self.options.with_openblas:
                self.requires.add('openblas/0.3.5@kudzurunner/stable')

    def configure(self):
        if self.settings.os == "Windows":
            self.options["openblas"].visual_studio=True
            self.options["openblas"].shared = True
        if self.options.with_jpeg:
            self.options["libjpeg-turbo"].shared = True
        if self.options.with_png:
            self.options["libpng"].shared = True
        if self.options.with_gif:
            self.options["giflib"].shared = True
        if self.options.with_sqlite3:
            self.options["sqlite3"].shared = True

    def source(self):
        archive_name = "v{}.tar.gz".format(self.version)
        url = "https://github.com/davisking/dlib/archive/{}".format(archive_name)
        tools.download(url, filename=archive_name)
        tools.untargz(filename=archive_name)
        os.remove(archive_name)

        tools.replace_in_file("{}/{}/CMakeLists.txt".format(self.source_name, self.name), "project(dlib)",
                              '''project(dlib)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_SHARED_LIBS'] = False if self.settings.compiler == "Visual Studio" else self.options.shared
        cmake.definitions['DLIB_JPEG_SUPPORT'] = self.options.with_jpeg
        cmake.definitions['DLIB_PNG_SUPPORT'] = self.options.with_png
        cmake.definitions['DLIB_GIF_SUPPORT'] = self.options.with_gif
        cmake.definitions['DLIB_USE_LAPACK'] = self.options.with_lapack
        cmake.definitions['DLIB_USE_BLAS'] = self.options.with_blas
        cmake.definitions['DLIB_LINK_WITH_SQLITE3'] = self.options.with_sqlite3
        cmake.definitions['DLIB_USE_CUDA'] = self.options.with_cuda
        cmake.definitions['DLIB_NO_GUI_SUPPORT'] = self.options.disable_gui
        cmake.definitions['DLIB_ISO_CPP_ONLY'] = self.options.enable_iso_cpp_only
        cmake.definitions['DLIB_ENABLE_STACK_TRACE'] = self.options.enable_stack_trace
        cmake.definitions['DLIB_ENABLE_ASSERTS'] = self.options.enable_assets
        cmake.definitions['USE_SSE2_INSTRUCTIONS'] = self.options.enable_sse2
        cmake.definitions['USE_SSE4_INSTRUCTIONS'] = self.options.enable_sse4
        cmake.definitions['USE_AVX_INSTRUCTIONS'] = self.options.enable_avx
        cmake.configure(source_folder=self.source_name)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include/dlib", src="{}/dlib".format(self.source_name))
        self.copy("config.h", dst="include/dlib", src="dlib")
        self.copy("revision.h", dst="include/dlib", src="dlib")
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.exe", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src=self.install_name, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=self.install_name, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=self.install_name, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
