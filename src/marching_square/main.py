from marching_square import MarchingSquare

def main():
    # change dim if you want (3d)
    marching_square = MarchingSquare(dim='2d', verbose=True)
    marching_square.run()


if __name__ == '__main__':
    main()
