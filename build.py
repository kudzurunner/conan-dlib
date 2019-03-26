from cpt.packager import ConanMultiPackager
import os

def disable_cuda(build):
    build.options.update({'dlib:with_cuda': False})
    return build

if __name__ == "__main__":
    builder = ConanMultiPackager(username="kudzurunner")
    builder.add_common_builds()
    if 'CONAN_VISUAL_VERSIONS' in os.environ:
        if os.environ['CONAN_VISUAL_VERSIONS'] == '15':
            builder.builds = map(disable_cuda, builder.items)
    builder.run()