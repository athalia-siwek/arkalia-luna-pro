# Installation d'Arkalia-LUNA

## Introduction

Bienvenue dans le guide d'installation d'Arkalia-LUNA, un système d'intelligence artificielle modulaire et local. Ce guide vous aidera à installer et configurer le système sur votre machine.

## Prérequis

Avant de commencer l'installation, assurez-vous d'avoir les éléments suivants :

- **Python 3.8+** : Assurez-vous que Python est installé et configuré sur votre système.
- **Docker** : Utilisé pour la conteneurisation des services.
- **Git** : Pour cloner le dépôt et gérer les versions du code.

## Étapes d'Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/arkalia-luna-system/arkalia-luna-pro.git
   cd arkalia-luna-pro
   ```

2. **Installer les dépendances Python**
   ```bash
   pip install -r requirements.txt
   ```

3. **Construire et lancer les conteneurs Docker**
   ```bash
   docker-compose up --build
   ```

## Configuration Post-Installation

- **Configurer les variables d'environnement** : Assurez-vous que toutes les variables d'environnement nécessaires sont définies.
- **Vérifier les logs** : Consultez les logs pour vous assurer que tous les services fonctionnent correctement.

## Dépannage

- **Problèmes de dépendances** : Si vous rencontrez des problèmes lors de l'installation des dépendances, vérifiez que vous utilisez la bonne version de Python.
- **Erreurs Docker** : Assurez-vous que Docker est en cours d'exécution et que vous avez les permissions nécessaires pour exécuter des conteneurs.

Pour plus d'informations, consultez la documentation complète ou contactez le support technique. 