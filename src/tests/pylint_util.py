from pylint import lint
import sys

print lint.Run.__doc__
pylint_arguments = ''

for arg in sys.argv[1:]:
    pylint_arguments+=(''+arg)

print pylint_arguments

lint.Run(sys.argv[1:])
