Finds cross-platform arbitrage between Polymarket, Kalshi, and PredictIt:
matches the same underlying event across platforms, and flags pairs where
buying the "Yes" side on one book and the "No" side on the other costs
less than $1 combined — a riskless-ish spread, since exactly one of the
two legs pays out $1 no matter what happens.  Make sure to double check results and that they are in fact the same market.  If you are betting on slightly different markets, then it will not pay out how you expected.  If the ROI is too good to be true, it probably is, this means the markets are slightly different and were incorrectly matched for arbitrages



pip install -r requirements.txt
cd backend
python app.py
