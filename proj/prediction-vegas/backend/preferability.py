def preferability(line, predict, o, u):
  dif = line - predict
  if dif > 0:
    bet_side = "under"
    bet_odds = u
    # we think lower than what vegas does, so we do the under
    safety = (100 * dif / predict) ** 1.5
    if abs(u) == u:
      pref = (safety) * ((u/100) + 1)
    else:
      u = abs(u)
      pref = (safety) * ((100/u) + 1)
  else:
    bet_side = "over"
    bet_odds = o
    # we think higher than what vegas does, so we do the under
    dif = abs(dif)
    safety = (100 * dif / predict) ** 1.5
    if abs(o) == o:
      pref = (safety) * ((o/100) + 1)
    else:
      o = abs(o)
      pref = (safety) * ((100/o) + 1)
  return pref, safety, bet_side, bet_odds
