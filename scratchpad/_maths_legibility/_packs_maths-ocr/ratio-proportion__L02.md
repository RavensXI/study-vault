# maths-ocr / ratio-proportion / L02 - Percentages & Compound Change

## bronze[0] (input: single_value, main-box unit: (none))
Q: Increase £200 by 10%.
   - intro: First the multiplier. An increase of 10% keeps the whole amount and adds a tenth, so add 0.10 to 1.
   - ask: Multiplier = 1 + 0.10 =  [box=1.1, NO label]
   - intro: Now multiply the original by the multiplier.
   - ask: 200 × 1.1 = £  [box=220, NO label]
   - intro: Check: the increase on its own should be 10% of 200.
   - ask: 220 − 200 = £  [box=20, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: Decrease £150 by 20%.
   - intro: First the multiplier. A decrease of 20% keeps 80% of the amount, so take 0.20 off 1.
   - ask: Multiplier = 1 − 0.20 =  [box=0.8, NO label]
   - intro: Now multiply the original by the multiplier.
   - ask: 150 × 0.8 = £  [box=120, NO label]
   - intro: Check: the amount lost should be 20% of 150.
   - ask: 150 − 120 = £  [box=30, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Find 25% of 60.
   - intro: 25% means 25 out of 100, which is a quarter.
   - ask: 25% as a decimal = 25 ÷ 100 =  [box=0.25, NO label]
   - intro: Multiply 60 by the decimal to find the part.
   - ask: 0.25 × 60 =  [box=15, NO label]
   - intro: Four lots of 25% should rebuild the whole 60.
   - ask: Check: 15 × 4 =  [box=60, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: A shirt costs £40. It is reduced by 10%. What is the sale price?
   - intro: First the multiplier. Reduced by 10% leaves 90% of the price, so take 0.10 off 1.
   - ask: Multiplier = 1 − 0.10 =  [box=0.9, NO label]
   - intro: Now multiply the original price by the multiplier.
   - ask: 40 × 0.9 = £  [box=36, NO label]
   - intro: Check: the discount should be 10% of 40.
   - ask: 40 − 36 = £  [box=4, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: What multiplier represents an increase of 5%?
   - intro: An increase keeps the whole original (100%) and adds the extra. First write 5% as a decimal.
   - ask: 5 ÷ 100 =  [box=0.05, label:'(a decimal)']
   - intro: An increase adds this to 1, the 100% you keep.
   - ask: 1 + 0.05 =  [box=1.05, NO label]
   - intro: Check by reading it back: a multiplier of 1.05 keeps 100% and adds how much?
   - ask: As a percentage, (1.05 − 1) × 100 =  [box=5, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: What multiplier represents a decrease of 30%?
   - intro: A decrease keeps what is left after taking the percentage away. First write 30% as a decimal.
   - ask: 30 ÷ 100 =  [box=0.3, label:'(a decimal)']
   - intro: A decrease takes this off 1, the 100% you started with.
   - ask: 1 − 0.3 =  [box=0.7, NO label]
   - intro: Check: how much has been taken off?
   - ask: Read it back: (1 − 0.7) × 100 =  [box=30, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: A price increases from £50 to £60. What is the percentage increase?
   - intro: Percentage change compares the change to what you started with. First find the actual change.
   - ask: Money change: 60 − 50 = £  [box=10, NO label]
   - intro: Now write the change as a fraction of the original price, not the new one.
   - ask: 10 ÷ 50 =  [box=0.2, label:'(a decimal)']
   - intro: Turn the decimal into a percentage.
   - ask: 0.2 × 100 =  [box=20, NO label]
   - intro: Check forwards: a 20% increase on 50 should land on 60.
   - ask: Check: 50 × 1.2 = £  [box=60, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Increase 300 by 50%.
   - intro: First the multiplier. An increase of 50% adds 0.5 to 1.
   - ask: Multiplier = 1 + 0.50 =  [box=1.5, NO label]
   - intro: Now multiply the original by the multiplier.
   - ask: 300 × 1.5 =  [box=450, NO label]
   - intro: Check: the increase should be 50% of 300.
   - ask: 450 − 300 =  [box=150, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: A TV costs £510 after a 15% increase. Find the original price.
   - intro: A reverse percentage. £510 is the price AFTER a 15% increase, so it is the original times the multiplier. Find that multiplier first.
   - ask: Multiplier = 1 + 0.15 =  [box=1.15, NO label]
   - intro: To undo the increase, divide the final price by the multiplier. Round to 2 d.p.
   - ask: 510 ÷ 1.15 = £  [box=443.48, NO label]
   - intro: Check by going forwards: the original plus 15% should return £510.
   - ask: Check: 443.48 × 1.15 = £  [box=510, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: £1000 earns 5% simple interest per year. How much interest after 3 years?
   - intro: Simple interest adds the same amount each year. First find one year's interest.
   - ask: One year: 1000 × 0.05 = £  [box=50, NO label]
   - intro: Simple interest does not compound, so just multiply by the number of years.
   - ask: 3 years: 50 × 3 = £  [box=150, NO label]
   - intro: Read it back: the account holds the original plus the interest.
   - ask: Check the total in the account: 1000 + 150 = £  [box=1150, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: A car worth £12000 depreciates by 10% per year. What is it worth after 1 year?
   - intro: Depreciation is a decrease. First the multiplier for losing 10%.
   - ask: Multiplier = 1 − 0.10 =  [box=0.9, NO label]
   - intro: Multiply the current value by the multiplier.
   - ask: 12000 × 0.9 = £  [box=10800, NO label]
   - intro: Check: the value lost should be 10% of 12000.
   - ask: 12000 − 10800 = £  [box=1200, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: After a 20% reduction, a coat costs £56. Find the original price.
   - intro: A reverse percentage. £56 is the price AFTER a 20% reduction, so it is the original times 0.80. Find that multiplier first.
   - ask: Multiplier = 1 − 0.20 =  [box=0.8, NO label]
   - intro: To undo the reduction, divide the final price by the multiplier.
   - ask: 56 ÷ 0.8 = £  [box=70, NO label]
   - intro: Check by going forwards: the original minus 20% should return £56.
   - ask: Check: 70 × 0.8 = £  [box=56, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: A population of 5000 increases by 2% each year. What is it after 1 year?
   - intro: Growth is an increase. First the multiplier for a 2% rise.
   - ask: Multiplier = 1 + 0.02 =  [box=1.02, NO label]
   - intro: Multiply the starting population by the multiplier.
   - ask: 5000 × 1.02 =  [box=5100, NO label]
   - intro: Check: the rise should be 2% of 5000.
   - ask: 5100 − 5000 =  [box=100, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: VAT is 20%. A laptop costs £480 before VAT. What is the price including VAT?
   - intro: Adding VAT is an increase. First the multiplier for adding 20%.
   - ask: Multiplier = 1 + 0.20 =  [box=1.2, NO label]
   - intro: Multiply the price before VAT by the multiplier.
   - ask: 480 × 1.2 = £  [box=576, NO label]
   - intro: Check: the VAT added should be 20% of 480.
   - ask: 576 − 480 = £  [box=96, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: A price drops from £80 to £64. What is the percentage decrease?
   - intro: Percentage change compares the drop to what you started with. First find the actual drop.
   - ask: Money drop: 80 − 64 = £  [box=16, NO label]
   - intro: Write the drop as a fraction of the original price, not the new one.
   - ask: 16 ÷ 80 =  [box=0.2, label:'(a decimal)']
   - intro: Turn the decimal into a percentage.
   - ask: 0.2 × 100 =  [box=20, NO label]
   - intro: Check forwards: a 20% decrease on 80 should land on 64.
   - ask: Check: 80 × 0.8 = £  [box=64, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: £3000 invested at 4% compound interest for 2 years. Find the final amount to 2 d.p.
   - intro: Compound interest is a repeated increase. First the yearly multiplier for 4%.
   - ask: Multiplier = 1 + 0.04 =  [box=1.04, NO label]
   - intro: It runs for 2 years, so raise the multiplier to the power 2.
   - ask: 1.04² =  [box=1.0816, NO label]
   - intro: Now multiply the starting amount by this single factor.
   - ask: 3000 × 1.0816 = £  [box=3244.8, NO label]
   - intro: Check the interest looks right for 2 years.
   - ask: Interest earned: 3244.80 − 3000 = £  [box=244.8, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: A car worth £15000 depreciates 12% per year. Value after 3 years? Round to nearest £.
   - intro: Depreciation is a repeated decrease. First the yearly multiplier for 12%.
   - ask: Multiplier = 1 − 0.12 =  [box=0.88, NO label]
   - intro: Over 3 years, raise the multiplier to the power 3.
   - ask: 0.88³ =  [box=0.681472, NO label]
   - intro: Multiply the starting value by this factor.
   - ask: 15000 × 0.681472 = £  [box=10222.08, NO label]
   - intro: The question asks for the nearest pound.
   - ask: Round to the nearest pound: £  [box=10222, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: After 2 years of 5% compound interest, an account has £1102.50. Find the original amount.
   - intro: A reverse compound problem. The final amount is the original times 1.05, twice over. First the yearly multiplier.
   - ask: Multiplier = 1 + 0.05 =  [box=1.05, NO label]
   - intro: Two years means the total factor is 1.05 squared.
   - ask: 1.05² =  [box=1.1025, NO label]
   - intro: Undo it by dividing the final amount by this factor.
   - ask: 1102.50 ÷ 1.1025 = £  [box=1000, NO label]
   - intro: Check by going forwards.
   - ask: Check: 1000 × 1.1025 = £  [box=1102.5, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: A population of 8000 decreases by 3% per year. After how many whole years is it first below 7000? (Enter the number of years.)
   - intro: The population loses 3% each year, so it multiplies by 0.97 every year. Test one year at a time.
   - ask: Multiplier for a 3% decrease = 1 − 0.03 =  [box=0.97, NO label]
   - intro: Work out year 4 first. Is it still above 7000?
   - ask: After 4 years: 8000 × 0.97⁴ =  [box=7082, NO label]
   - intro: 7082 is still above 7000, so go one more year.
   - ask: After 5 years: 8000 × 0.97⁵ =  [box=6870, NO label]
   - intro: Year 5 is the first below 7000.
   - ask: The first whole year below 7000 is year  [box=5, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: £500 earns 6% compound interest. How much interest (not total) after 2 years? To 2 d.p.
   - intro: Compound interest. First the yearly multiplier for 6%.
   - ask: Multiplier = 1 + 0.06 =  [box=1.06, NO label]
   - intro: Two years, so raise the multiplier to the power 2.
   - ask: 1.06² =  [box=1.1236, NO label]
   - intro: Find the total amount first.
   - ask: Total: 500 × 1.1236 = £  [box=561.8, NO label]
   - intro: The question wants the interest, not the total, so subtract the starting amount.
   - ask: Interest only: 561.80 − 500 = £  [box=61.8, NO label]
