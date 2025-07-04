#!/usr/bin/env python3
"""
📚 Script de vérification de la documentation
📝 Vérifie la qualité et la complétude de la documentation
🔧 Version: 2.8.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

import ast
import sys
from pathlib import Path


class DocChecker:
    """Vérificateur de documentation."""

    def __init__(self):
        self.issues = []
        self.stats = {
            "files_checked": 0,
            "functions_with_docs": 0,
            "functions_without_docs": 0,
            "classes_with_docs": 0,
            "classes_without_docs": 0,
            "modules_with_docs": 0,
            "modules_without_docs": 0,
        }

    def check_file(self, file_path: Path) -> None:
        """Vérifie un fichier Python."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            self.stats["files_checked"] += 1

            # Vérifier la docstring du module
            module_doc = ast.get_docstring(tree)
            if module_doc:
                self.stats["modules_with_docs"] += 1
            else:
                self.stats["modules_without_docs"] += 1
                self.issues.append(f"📝 {file_path}: Module sans docstring")

            # Vérifier les classes et fonctions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self._check_function(node, file_path)
                elif isinstance(node, ast.ClassDef):
                    self._check_class(node, file_path)

        except Exception as e:
            self.issues.append(f"❌ {file_path}: Erreur d'analyse - {e}")

    def _check_function(self, node: ast.FunctionDef, file_path: Path) -> None:
        """Vérifie une fonction."""
        # Ignorer les méthodes privées et les tests
        if node.name.startswith("_") or "test" in node.name.lower():
            return

        doc = ast.get_docstring(node)
        if doc:
            self.stats["functions_with_docs"] += 1
        else:
            self.stats["functions_without_docs"] += 1
            self.issues.append(
                f"📝 {file_path}:{node.lineno} - Fonction '{node.name}' sans docstring"
            )

    def _check_class(self, node: ast.ClassDef, file_path: Path) -> None:
        """Vérifie une classe."""
        # Ignorer les classes privées et les tests
        if node.name.startswith("_") or "test" in node.name.lower():
            return

        doc = ast.get_docstring(node)
        if doc:
            self.stats["classes_with_docs"] += 1
        else:
            self.stats["classes_without_docs"] += 1
            self.issues.append(
                f"📝 {file_path}:{node.lineno} - Classe '{node.name}' sans docstring"
            )

    def generate_report(self) -> str:
        """Génère un rapport de vérification."""
        total_functions = self.stats["functions_with_docs"] + self.stats["functions_without_docs"]
        total_classes = self.stats["classes_with_docs"] + self.stats["classes_without_docs"]
        total_modules = self.stats["modules_with_docs"] + self.stats["modules_without_docs"]

        report = [
            "📚 RAPPORT DE VÉRIFICATION DE DOCUMENTATION",
            "=" * 50,
            f"📁 Fichiers vérifiés: {self.stats['files_checked']}",
            "",
            "📊 Statistiques:",
            f"  📝 Modules avec docstring: {self.stats['modules_with_docs']}/{total_modules}",
            f"  📝 Classes avec docstring: {self.stats['classes_with_docs']}/{total_classes}",
            f"  📝 Fonctions avec docstring: {self.stats['functions_with_docs']}/{total_functions}",
            "",
        ]

        if total_functions > 0:
            func_coverage = (self.stats["functions_with_docs"] / total_functions) * 100
            report.append(f"📈 Couverture fonctions: {func_coverage:.1f}%")

        if total_classes > 0:
            class_coverage = (self.stats["classes_with_docs"] / total_classes) * 100
            report.append(f"📈 Couverture classes: {class_coverage:.1f}%")

        if self.issues:
            report.extend(["", "⚠️ Problèmes détectés:", *self.issues])
        else:
            report.append("✅ Aucun problème détecté!")

        return "\n".join(report)


def main():
    """Fonction principale."""
    checker = DocChecker()

    # Vérifier les modules
    modules_dir = Path("modules")
    if not modules_dir.exists():
        print("❌ Répertoire modules/ non trouvé")
        sys.exit(1)

    print("🔍 Vérification de la documentation...")

    for py_file in modules_dir.rglob("*.py"):
        if not py_file.name.startswith("__"):
            checker.check_file(py_file)

    # Générer le rapport
    report = checker.generate_report()
    print(report)

    # Retourner un code d'erreur si des problèmes sont détectés
    has_issues = len(checker.issues) > 0
    if has_issues:
        print(f"\n⚠️ {len(checker.issues)} problème(s) de documentation détecté(s)")

    sys.exit(1 if has_issues else 0)


if __name__ == "__main__":
    main()
