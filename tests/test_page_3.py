# test_page_3.py

import dash.testing.wait as wait
import dash.testing.browser

def test_page_3():
    # Créez une instance de navigateur Dash
    browser = dash.testing.browser.Dash(__name__)
    browser.server.app.config.suppress_callback_exceptions = True

    # Chargez la page de la page 3 (assurez-vous que l'URL est correcte)
    browser.visit('/page-3')

    # Attendez que la page soit complètement chargée (vous pouvez ajuster le délai si nécessaire)
    wait.until(lambda: len(browser.find_elements("div#top-10-features-importance-radar-chart")) > 0)

    # Effectuez des assertions pour vérifier le contenu de la page
    assert "Top 10 Features Importance Radar Chart" in browser.title
    assert len(browser.find_elements("div#top-10-features-importance-radar-chart")) > 0

    # Fermez le navigateur
    browser.quit()
