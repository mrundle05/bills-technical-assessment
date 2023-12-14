-- To get the blitz rate by game
SELECT P.pff_OFFTEAM AS 'Opponent', SUM(P.pff_BLITZDOG)/COUNT(*) AS 'Blitz Rate'
FROM tblPlays P
WHERE P.pff_DEFTEAM = 'TEN'
GROUP BY P.pff_GAMEID, P.pff_OFFTEAM
ORDER BY SUM(P.pff_BLITZDOG)/COUNT(*);

-- To get the score for each game, which can tell whether the Titans won or lost
SELECT 
   CASE
        WHEN P.pff_OFFTEAM = 'TEN' AND P.pff_DRIVEENDEVENT = 'TOUCHDOWN' THEN P.pff_OFFSCORE + 7
        WHEN P.pff_OFFTEAM = 'TEN' AND P.pff_KICKRESULT LIKE 'MADE%' THEN P.pff_OFFSCORE + 3
        WHEN P.pff_DEFTEAM = 'TEN' THEN P.pff_DEFSCORE
        ELSE P.pff_OFFSCORE
    END AS 'TEN SCORE',
   CASE
        WHEN P.pff_OFFTEAM <> 'TEN' AND P.pff_DRIVEENDEVENT = 'TOUCHDOWN' THEN P.pff_OFFSCORE + 7
        WHEN P.pff_OFFTEAM <> 'TEN' AND P.pff_KICKRESULT LIKE 'MADE%' THEN P.pff_OFFSCORE + 3
        WHEN P.pff_DEFTEAM <> 'TEN' THEN P.pff_DEFSCORE
        ELSE P.pff_OFFSCORE
    END AS 'OPPONENT SCORE'
FROM tblPlays P
-- Where it is the last play of the game
WHERE P.pff_PLAYID IN(
    SELECT MAX(P2.pff_PLAYID)
    FROM tblPlays P2
    GROUP BY P2.pff_GAMEID
);

-- To get the turnover differential for each game
SELECT 
    P.pff_WEEK,
    SUM(CASE WHEN P.pff_OFFTEAM = 'TEN' AND (P.pff_FUMBLE = 1 OR P.pff_INTERCEPTION = 1) THEN 1 ELSE 0 END) -
    SUM(CASE WHEN P.pff_DEFTEAM = 'TEN' AND (P.pff_FUMBLE = 1 OR P.pff_INTERCEPTION = 1) THEN 1 ELSE 0 END) AS 'TURNOVER DIFFERENTIAL'
FROM tblPlays P
GROUP BY P.pff_WEEK;
