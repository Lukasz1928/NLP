The task is to:
1. Find all external references to bills, e.g. **ustawie z dnia 
   4 marca 1994 r. o zakładowym funduszu świadczeń socjalnych (Dz. U.  z 2012 r. poz. 592)**.
   The result should be aggregated by bill ID (year and position) and sorted by descending number of reference
   counts. The reference format should include:
   * the title of the regulation (if present)
   * the year of the regulation
   * the number of the Journal of Laws of the Republic of Poland (*Dziennik Ustaw*) - if applicable
   * the position of the regulation
1. Find all internal references to regulations, e.g.  **art.  5 ust. 2**, **art. 5 ust. 7**, etc. The result should
   exclude the internal numbering of the bill (e.g. **Art. 1.** W ustawie ...).
   The result should be aggregated by regulation ID (as described below) and sorted by descending number of reference
   counts inside particular bill. The bills should be sorted by descending number of internal references. 
   The reference format should include all elements necessary to identify the regulation, e.g.:
   * art. 1, ust. 2 - if an article inside the regulation is referenced,
   * ust. 2 - if a paragraph inside the same article is referenced,
   * etc.
1. Count all occurrences of the word **ustawa** in all inflected forms (*ustawa*, *ustawie*, *ustawę*, etc.),
   and all spelling forms (*ustawa*, *Ustawa*, *USTAWA*), excluding other words with the same prefix (e.g. *ustawić*).