from aqt import mw
from aqt.qt import QAction, qconnect
from aqt.utils import showInfo

def delete_empty_decks():
    empty_decks = []
    for deck_id, deck in mw.col.decks.decks.items():
        deck_name = deck['name']
        card_count = mw.col.db.scalar(
            "select count() from cards where did = ?", deck_id
        )
        if card_count == 0:
            empty_decks.append(deck_name)
            mw.col.decks.rem(deck_id)

    if empty_decks:
        mw.col.decks.save()
        mw.col.decks.flush()
        mw.reset()
        showInfo(f"Deleted empty decks: {', '.join(empty_decks)}")
    else:
        showInfo("No empty decks found")

action = QAction("Delete Empty Decks", mw)
qconnect(action.triggered, delete_empty_decks)
mw.form.menuTools.addAction(action)
