# stock-market-alert

### Work in progress

---

### Système d'alerting sur des cours de bourses en serverless

## Fonctionnalités 
  * Alerte par SMS sur une variation à la hausse ou à la baisse depuis la dernière alerte
  * Composé uniquement de services serverless
  * Alerte comprenant un lien vers l'application bourse Apple

## Utilisation
* [Créer et importer la couche pour le package yahooquery](https://tristanlanoy.com/post/aws-lambda-py-packages/)
* Créer la base DynamoDb (aws --profile=via dynamodb create-table --cli-input-json dynamodb/stock_db.json)
* Configurer une rubrique SNS et la renseigner dans le code de la fonction Lambda
* Importer la fonction lambda
* Créer une règle EventBridge pour exécuter la fonction lambda de façon planifiée

## Informations
Le pourquoi du comment ainsi que le cheminenent détaillé se trouve [sur mon blog](https://tristanlanoy.com/post/stock-alert/)

## TODO
* Améliorer le code de la fonction lambda
* Mettre en place une UI pour l'ajout des alertes
* Mettre en place un systèle permettant de réactualiser le champ base price
* Simplifier le déploiement
* Améliorer la documentation
* Mettre en place du CI/CD