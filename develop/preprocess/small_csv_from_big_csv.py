import sys
from getopt import getopt, GetoptError

class MakeCsvSample():

    _short_options = 'o:l:'
    _long_options = ['output=', 'line=']
    _minimum_number_of_arguments = 1

    def __init__(self):
        self.options_list = self.get_command_line_options()
        self.check_csv_input_or_err(sys.argv[1:])

    def get_command_line_options(self):
        return sys.argv[2:]

    def check_csv_input_or_err(self, args):
        if len(args) < self._minimum_number_of_arguments:
            print('Invalid option -- no .csv input')
            print('CSV file name is mandatory.')
            sys.exit(1)
        csv_name = args[0]
        if not csv_name.endswith('.csv'):
            print('Invalid option -- input is not a .csv')
            sys.exit(1)

    def parse_command_line_options(self):
        try:
            opts, args = getopt(self.options_list, self._short_options, self._long_options)

            if len(args) > 0:
                print('Invalid option -- unknown commands.')
                print('Invalid arguments: {}'.format(args))
                sys.exit(1)

            return opts
        except GetoptError as err:
            print(err)
            sys.exit(1)

    def parse_and_execute_commands(self):
        opts = self.parse_command_line_options()
        for command, argument in opts:
            print('command = {}'.format(command))
            print('argument = {}'.format(argument))

if __name__ == '__main__':
    make_csv_sample = MakeCsvSample()
    make_csv_sample.parse_and_execute_commands()
