# Quantum_Chess
This game is like normal chess, but you have the ability to quantumly superimpose your pieces, splitting into a real and fake version of the piece. Your opponent can only see that it is split; they cannot see which option is real or fake. Like the classic quantum superposition thought experiment, Schrödinger's cat, you can only find out which of the options is real when you interact with the system (take either of the pieces). To win the game, you must capture the king; there are no check or checkmate conditions in this game, as it would enable the user to deduce which of the superimposed pieces is real or fake, taking away the fun. The act of splitting a piece takes a move. You may move both split pieces during the same turn.


Bugs to fix:

On developer view (show true) it doesn't show the false pieces. This is not what i want. What i instead want is it to show the image of the full piece on top of the true piece and the split piece on top of the split piece (the same as what that player would see if theyre his pieces). The opponent of the split piece should see two split images, not knowing which one is real.

Castling doesn't work - fix: add a button to castle or add it to legalK

When moving split pieces, it makes you select the real piece then its destination, then choose the fake piece and its destination. When they are on top of each other, you choose the destination for the real piece but it doesn't move out of the way. This makes it impossible to select and move the fake piece under it, so you get soft locked.


To start it:

python app.py |then| ctrl + click (the link they give you)