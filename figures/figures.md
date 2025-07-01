# Notizen zu den Figuren

1. **Plots im figures Ordner**:
   Die Plots sind nun im "figures" Ordner zu finden. Es handelt sich um 4 Plots, die nebeneinander in einer Figur dargestellt sind.

2. **Beschreibung der Plots (von links nach rechts)**:
   - Distribution updates
   - Rollouts
   - Exploration curve
   - Learning curve.

3. **Probleme mit bestimmten Plots**:
   Die Plots, die zuvor Fehler angezeigt haben, sind der zweite und der letzte Plot rechts.

4. **Rollouts Plot** (der zweite):
   Beim Rollouts Plot verhielt sich der Code merkwürdig. Der Fehler wurde durch diese Zeile verursacht: [Link zur Codezeile](https://scm.cms.hu-berlin.de/adapt/teaching/ws23-smlr/g4-user_feedback/-/blob/main/dmpbbo/bbo_of_dmps/LearningSessionTask.py?ref_type=heads#L143).
   Ich habe das Problem vorläufig gelöst, indem ich diese Zeile auskommentiert und in der darauf folgenden Zeile neu implementiert habe. Der Plot ist jedoch noch schwer zu interpretieren. Ich werde noch, einen Titel hinzuzufügen und möglicherweise eine Legende einzufügen, sobald ich den Plot besser verstehe.

5. **Lernkurve Plot** (der vierte):
   Der Debugging-Prozess für den Plot der Lernkurve war etwas schwieriger. Der ursprüngliche Fehler lag hier: [Link zur Codezeile](https://scm.cms.hu-berlin.de/adapt/teaching/ws23-smlr/g4-user_feedback/-/blob/main/dmpbbo/bbo/LearningSession.py?ref_type=heads#L531) (wo `c` als Element nicht weiter indiziert werden kann). Neben dieser Zeile steht jedoch "# Only include sum", also habe ich selbst alle Kosten mit korrekten Syntax addiert, wie es in der nächsten Zeile (Zeile 532) zu sehen ist.
   Die Kosten für ein Update sind daher die Summe der Zahlen von 1 bis 5 (und wir haben 7 Updates). Der Plot wird unter `distr_rollouts_explor_lc__2A.png` gespeichert. Ich habe die Simulation erneut durchgeführt, und der resultierende Plot ist unter `distr_rollouts_explor_lc__2B.png` gespeichert (ich war nur skeptisch da-- also kann weg).

   Nachträglich habe ich gesehen, dass nur das erste Element der Kostenliste genutzt wird, wie hier erwähnt: [Link zur Codezeile](https://scm.cms.hu-berlin.de/adapt/teaching/ws23-smlr/g4-user_feedback/-/blob/main/dmpbbo/bbo/LearningSession.py?ref_type=heads#L489).
   Dies erklärt, warum versucht wurde, auf die Kostenliste mit `c[0]` zuzugreifen. Ich habe das ebenfalls ausprobiert, indem ich es als alternative Option fuer die Summe. Diese Option ist erstaml auskommentiert gelassen: [Link zur Codezeile](https://scm.cms.hu-berlin.de/adapt/teaching/ws23-smlr/g4-user_feedback/-/blob/main/dmpbbo/bbo/LearningSession.py?ref_type=heads#L533).
   Das Ergebnis dieses Versuchs ist unter `distr_rollouts_explor_lc__1A.png.png` gespeichert. Ich habe die Simulation erneut durchgeführt, und der resultierende Plot ist unter `distr_rollouts_explor_lc__1B.png` gespeichert.


Zusammengefasst können wir entweder die Kosten eines Update-Schrittes aufsummieren oder das erste Element aus der Kostenliste eines Update-Schrittes als Repräsentanten nehmen.

Ausserdem muss ich erwaehnen, dass eine Funktion fuer die Lernkurve Plot gar nicht existiert, also muesste ich einige Sachen weglassen. Hier ist ein Beispiel: [Link zur Codezeile](https://scm.cms.hu-berlin.de/adapt/teaching/ws23-smlr/g4-user_feedback/-/blob/main/dmpbbo/bbo/LearningSession.py?ref_type=heads#L507).

Die `get_cost_labels()`Funktion habe ich niergendwo gefunden und habe ihre Rueckgabe mit einer leeren Liste ersetzt.