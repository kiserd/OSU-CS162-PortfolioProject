# Author: Donald Logan Kiser
# Date: 05/21/2020
# Description: Unit tests for GessGame.py

import unittest
from GessGame import GessGame, Board


class CountSeqTests(unittest.TestCase):
    """
    define unit tests for GessGame.py
    """

    def test_1(self):
        """
        test attempt to move piece too far
        """
        gg = GessGame()
        self.assertFalse(gg.make_move('r6', 'r13'))

    def test_2(self):
        """
        test attempt to move piece through an obstruction
        """
        gg = GessGame()
        self.assertFalse(gg.make_move('j3', 'j10'))

    def test_3(self):
        """
        test whether turn changes to opposing player at the end of the turn
        """
        gg = GessGame()
        gg.make_move('i3', 'i5')
        board = gg.get_board()
        board_list = board.get_board()
        self.assertFalse(gg.get_black_turn())

        # board_list = board.get_board()
        # for row in board_list:
        #     print(row)
        # print(gg.get_game_state())

    def test_4(self):
        """
        test valid move by both players and GessGame._black_turn value after each valid turn
        """
        gg = GessGame()
        self.assertTrue(gg.make_move('r3', 'r4'))
        self.assertFalse(gg.get_black_turn())
        self.assertTrue(gg.make_move('i18', 'i17'))
        self.assertTrue(gg.get_black_turn())

        # board = gg.get_board()
        # board_list = board.get_board()
        # for row in board_list:
        #     print(row)
        # print(gg.get_game_state())

    def test_5(self):
        """
        test several invalid moves by both players
        """
        gg = GessGame()
        self.assertFalse(gg.make_move('i3', 'i12'))
        self.assertFalse(gg.make_move('i6', 'i12'))
        self.assertFalse(gg.make_move('r3', 'o3'))
        self.assertFalse(gg.make_move('c3', 'd4'))
        self.assertFalse(gg.make_move('h3', 'g3'))
        self.assertFalse(gg.make_move('l3', 'l9'))
        self.assertFalse(gg.make_move('c3', 'c1'))
        self.assertFalse(gg.make_move('f3', 'h5'))
        self.assertFalse(gg.make_move('r3', 't3'))
        self.assertTrue(gg.make_move('l3', 'l5'))

        self.assertFalse(gg.get_black_turn())
        self.assertFalse(gg.make_move('i18', 'i11'))
        self.assertFalse(gg.make_move('i15', 'i9'))
        self.assertFalse(gg.make_move('r18', 'o18'))
        self.assertFalse(gg.make_move('c18', 'd17'))
        self.assertFalse(gg.make_move('h18', 'g18'))
        self.assertFalse(gg.make_move('l18', 'l14'))
        self.assertFalse(gg.make_move('c18', 'c20'))
        self.assertFalse(gg.make_move('f18', 'h16'))
        self.assertTrue(gg.make_move('l18', 'l16'))

        self.assertTrue(gg.get_black_turn())

        # board = gg.get_board()
        # board_list = board.get_board()
        # for row in board_list:
        #     print(row)
        # print(gg.get_game_state())

    def test_6(self):
        """
        test victorious sequence
        """
        gg = GessGame()
        self.assertTrue(gg.make_move('m7', 'k7'))
        self.assertTrue(gg.make_move('j14', 'h14'))
        self.assertTrue(gg.make_move('n7', 'p7'))
        self.assertTrue(gg.make_move('i18', 'i9'))
        self.assertTrue(gg.make_move('f6', 'f7'))
        self.assertTrue(gg.make_move('i9', 'l9'))
        self.assertTrue(gg.make_move('f7', 'f8'))
        self.assertTrue(gg.make_move('l9', 'l5'))
        self.assertEqual(gg.get_game_state(), 'WHITE_WON')
        self.assertFalse(gg.make_move('f8', 'f9'))

        # board = gg.get_board()
        # board_list = board.get_board()
        # for row in board_list:
        #     print(row)


if __name__ == '__main__':
    unittest.main()