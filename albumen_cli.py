from optparse import OptionParser
import logging

import albumen_backend

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    parser = OptionParser()
    parser.add_option('-s', dest='size')
    parser.add_option('-a', dest='aspect', default='complexity')
    parser.add_option('-d', dest='data', default='static/albumen/data')
    parser.add_option('-n', dest='num', type='int', default=100)

    options, args = parser.parse_args()

    width, height = map(int, options.size.split('x'))   
 
    albumen_backend.gen_bg(source=options.data, sortfield=options.aspect, 
        width=width, height=height, num=options.num)

if __name__ == '__main__':
    main()
