from modules.trade import Trade


def calculate_profit_loss(
    trades_list: list[Trade],
) -> tuple[float, float, int, int]:
    """
    Calculates the number of profitable and losing trades.

    Args:
        trades_list (list[Trade]): A list of Trade objects representing trades.

    Returns:
        A tuple containing the number of profitable trades and losing trades
        and total profit/loss percent.
    """
    profit = 0
    loss = 0
    profit_percent = 0
    loss_percent = 0
    for i in range(len(trades_list)):
        trade = trades_list[i]
        target = "SHORT" if trade.side == "LONG" else "LONG"

        for j in range(i + 1, len(trades_list)):
            next_trade = trades_list[j]
            if next_trade.side == target:
                if trade.side == "LONG":
                    if trade.entry_order_price < next_trade.entry_order_price:
                        profit += 1
                        profit_percent += (
                            next_trade.entry_order_price / trade.entry_order_price - 1
                        ) * 100
                        trade.trade_results = (
                            next_trade.entry_order_price - trade.entry_order_price
                        ) * trade.trade_quantity
                    else:
                        loss += 1
                        loss_percent += (
                            trade.entry_order_price / next_trade.entry_order_price - 1
                        ) * 100
                        trade.trade_results = (
                            -(trade.entry_order_price - next_trade.entry_order_price)
                            * trade.trade_quantity
                        )

                elif trade.side == "SHORT":
                    if trade.entry_order_price > next_trade.entry_order_price:
                        profit += 1
                        profit_percent += (
                            trade.entry_order_price / next_trade.entry_order_price - 1
                        ) * 100
                        trade.trade_results = (
                            trade.entry_order_price - next_trade.entry_order_price
                        ) * trade.trade_quantity
                    else:
                        loss += 1
                        loss_percent += (
                            next_trade.entry_order_price / trade.entry_order_price - 1
                        ) * 100
                        trade.trade_results = (
                            -(next_trade.entry_order_price - trade.entry_order_price)
                            * trade.trade_quantity
                        )
                break

    if not loss_percent:
        loss_percent = 1.0

    return profit_percent, loss_percent, profit, loss


def get_greatest_drop(
        balance_change_history: list[float],
) -> tuple[float, int, int]:
    """
    Calculate the greatest drop in a balance change history
    and return the drop percentage, start index and end index of the drop.

    Args:
        balance_change_history (list[float]): List of balance change values.

    Returns:
        Greatest drop percentage, start index and end index of the drop.
    """

    min_val = None  # Minimum balance value
    min_i = None  # Index of the minimum balance value
    greatest_drop = None  # Greatest drop percentage
    greatest_drop_start = None  # Start index of the greatest drop
    greatest_drop_end = None  # End index of the greatest drop
    # Iterate through the balance change history in reverse order
    for i in range(len(balance_change_history) - 1, -1, -1):
        if min_val is None or balance_change_history[i] < min_val:
            min_val = balance_change_history[i]
            min_i = i

        drop = 1 - min_val / balance_change_history[i]
        # Check if the current drop is greater than the greatest drop
        if greatest_drop is None or drop > greatest_drop:
            greatest_drop = drop
            greatest_drop_start = i
            greatest_drop_end = min_i

    return greatest_drop * 100, greatest_drop_start, greatest_drop_end

