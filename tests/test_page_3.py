import dash.testing.wait as wait
import dash.testing.browser

def test_page_3():
    # Créez une instance de navigateur Dash
    browser = dash.testing.browser.Dash(__name__)
    browser.server.app.config.suppress_callback_exceptions = True

    # Chargez la page principale de votre application Dash
    browser.visit('https://dewanoupredict-9816cc161f92.herokuapp.com/')

    # Ajoutez du code pour naviguer vers l'onglet Page 3 (l'onglet doit être identifié par son texte)
    browser.driver.find_element_by_link_text("Page 3").click()

    # Attendez que la page soit complètement chargée (vous pouvez ajuster le délai si nécessaire)
    wait.until(lambda: len(browser.find_elements("div#top-10-features-importance-radar-chart")) > 0)

    # Effectuez des assertions pour vérifier le contenu de la page
    assert "Top 10 Features Importance Radar Chart" in browser.title
    assert len(browser.find_elements("div#top-10-features-importance-radar-chart")) > 0

    # Fermez le navigateur
    browser.quit()
