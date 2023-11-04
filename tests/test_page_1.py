import dash.testing.wait as wait
import dash.testing.browser

def test_page_1():
    # Créez une instance de navigateur Dash
    browser = dash.testing.browser.Dash(__name__)
    browser.server.app.config.suppress_callback_exceptions = True

    # Chargez la page de la page 1 en utilisant l'URL correcte
    browser.visit('https://dewanoupredict-9816cc161f92.herokuapp.com/')

    # Attendez que la page soit complètement chargée (vous pouvez ajuster le délai si nécessaire)
    wait.until(lambda: len(browser.find_elements("#sk-id-dropdown")) > 0)

    # Effectuez des assertions pour vérifier le contenu de la page
    assert "Prédiction de la Solvabilité du Client" in browser.title
    assert len(browser.find_elements("#sk-id-dropdown")) > 0

    # Fermez le navigateur
    browser.quit()
