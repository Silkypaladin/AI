import gui
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from game import *

class Game(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.game = Board()
        self.window = gui.Ui_MainWindow()
        self.window.setupUi(self)
        self.window.label.setHidden(True)
        self.updateUI()
        self.show()
        self.window.moveHole1.clicked.connect(lambda: self.move_stones_button_clicked(1))
        self.window.moveHole2.clicked.connect(lambda: self.move_stones_button_clicked(2))
        self.window.moveHole3.clicked.connect(lambda: self.move_stones_button_clicked(3))
        self.window.moveHole4.clicked.connect(lambda: self.move_stones_button_clicked(4))
        self.window.moveHole5.clicked.connect(lambda: self.move_stones_button_clicked(5))
        self.window.moveHole6.clicked.connect(lambda: self.move_stones_button_clicked(6))
        self.window.nextTurn.clicked.connect(lambda: self.next_turn_button_clicked())
        # self.window.next_move.clicked.connect(lambda: self.opposite_player_move())
        # self.window.start.clicked.connect(lambda: self.reset_game())

    def updateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.window.hole12.setText(_translate("MainWindow", str(self.game.holes[13].stones)))
        self.window.hole11.setText(_translate("MainWindow", str(self.game.holes[12].stones)))
        self.window.hole10.setText(_translate("MainWindow", str(self.game.holes[11].stones)))
        self.window.hole9.setText(_translate("MainWindow", str(self.game.holes[10].stones)))
        self.window.hole8.setText(_translate("MainWindow", str(self.game.holes[9].stones)))
        self.window.hole7.setText(_translate("MainWindow", str(self.game.holes[8].stones)))
        self.window.hole1.setText(_translate("MainWindow", str(self.game.holes[1].stones)))
        self.window.hole2.setText(_translate("MainWindow", str(self.game.holes[2].stones)))
        self.window.hole3.setText(_translate("MainWindow", str(self.game.holes[3].stones)))
        self.window.hole4.setText(_translate("MainWindow", str(self.game.holes[4].stones)))
        self.window.hole5.setText(_translate("MainWindow", str(self.game.holes[5].stones)))
        self.window.hole6.setText(_translate("MainWindow", str(self.game.holes[6].stones)))
        self.window.well1.setText(_translate("MainWindow", str(self.game.holes[0].stones)))
        self.window.well2.setText(_translate("MainWindow", str(self.game.holes[7].stones)))
        self.window.moveHole1.setText(_translate("MainWindow", "Move Hole 1"))
        self.window.moveHole2.setText(_translate("MainWindow", "Move Hole 2"))
        self.window.moveHole3.setText(_translate("MainWindow", "Move Hole 3"))
        self.window.moveHole4.setText(_translate("MainWindow", "Move Hole 4"))
        self.window.moveHole5.setText(_translate("MainWindow", "Move Hole 5"))
        self.window.moveHole6.setText(_translate("MainWindow", "Move Hole 6"))
        if self.game.player_turn == PLAYER_ONE:
            self.window.player_turn.setText(_translate("MainWindow", "Player's 1 turn"))
            self.window.nextTurn.setEnabled(False)
            self.change_buttons_availability(True)
        else:
            self.window.player_turn.setText(_translate("MainWindow", "Player's 2 turn"))
            self.change_buttons_availability(False)
            self.window.nextTurn.setEnabled(True)

    def change_buttons_availability(self, availability):
        self.window.moveHole1.setEnabled(availability)
        self.window.moveHole2.setEnabled(availability)
        self.window.moveHole3.setEnabled(availability)
        self.window.moveHole4.setEnabled(availability)
        self.window.moveHole5.setEnabled(availability)
        self.window.moveHole6.setEnabled(availability)

    def move_stones_button_clicked(self, hole_number):
        if self.game.holes[hole_number].stones > 0:
            hole_after_move, is_finished = self.game.move_stones_from_hole(hole_number)

            if is_finished:
                self.game_finished()
                return
            self.game.decide_turn(hole_after_move)
            self.updateUI()

    def next_turn_button_clicked(self):
        self.game.ai_minimax_move(3)
        is_finished = self.game.check_if_the_game_is_finished()
        if is_finished:
            self.game_finished()
            return
        self.updateUI()

    def game_finished(self):
        print('The game has ended!')
        self.updateUI()
        score_p1 = self.game.holes[7].stones
        score_p2 = self.game.holes[0].stones
        print('Player\'s one score: ', score_p1)
        print('Player\'s two score: ', score_p2)
        if score_p1 > score_p2:
            self.window.label.setText(f"Game Over! Player one won with score: {score_p1}")
        elif score_p2 > score_p1:
            self.window.label.setText(f"Game Over! Player two won with score: {score_p2}")
        else:
            self.window.label.setText(f"Game Over! It is a draw.")
        self.window.label.setHidden(False)
        self.change_buttons_availability(False)
        self.window.nextTurn.setEnabled(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())