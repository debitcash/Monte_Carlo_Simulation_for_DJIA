### Predictive Algorithm for Equities 
Created after completion of a quantitative finance course with the Société Financiers educational group.

The project comprises three key components: Equity.py (the description of the Equity object representing the DJIA), LIB_SFQ_Vanilla_MC_Fns.py (containing all statistical logic), and RunAlgorithm.py (executing all data manipulations).

It employs a swing trading approach based on Monte Carlo Random Simulation, by forecasting prices over the weekend and executing 'buy' trades at the week's start, closing them at its end.


The algorithm's general logic is as follows:

&bullet; Get previous year prices.

&bullet; Compute volatility and standard deviation on received data.

&bullet; Generate a random normal distribution, where previously calculated volatility and standard deviation serve as fundamental parameters.

&bullet; Iterate 10,000 times, selecting a random number from the mentioned distribution for each day of the week, resulting in a matrix formatted as 10000xMTWThF.

&bullet; Apply the generated return values to the consecutive days starting with previous Friday, thus forming a matrix showing 10,000 values of projected prices for each day.

&bullet; Choose a single predicted value for the next week's last day, based on the 50th percentile.



During usage, this method proved inefficient due to its static nature. Predicted values tended to be uniform and heavily reliant on last year's data, resulting in minimal predictive efficacy as the previous year's upward trend overly influenced predictions, always yielding 'go long' signals. Therefore, I refined the logic to limit the 'go long' action only to instances where the last two weeks' values were lower than the current week.

<br>

>[!IMPORTANT]
>The base logic yields a yearly return of **2%** with a 0.02% risk set in the form of manual stop-loss.<br>
>Following the update, the logic achieves a **7%** yearly return, while maintaining the 0.02% risk level through manual stop-loss implementation.
<div align="center">
<img src="https://raw.githubusercontent.com/debitcash/Trading-robot/master/Results.png">
</div>
