import os
import argparse
import json
import subprocess
from pathlib import Path
from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring, indent
from typing import List, Dict


class AdvancedQRCGenerator:
    def __init__(self, config_file='qrc_config.json'):
        self.config = self.load_config(config_file)
        self.project_root = Path(self.config.get('project_root', '.'))
        self.output_file = self.config.get('output_file', 'resources.qrc')
        self.include_patterns = self.config.get('include_patterns', [
            '*.ico', '*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp',
            '*.svg', '*.css', '*.qss', '*.qm', '*.ttf', '*.otf',
            '*.json', '*.xml', '*.txt'
        ])
        self.exclude_patterns = self.config.get('exclude_patterns', [
            '__pycache__', '.git', '.vscode', '.idea', 'venv', 'env',
            'node_modules', 'dist', 'build', '*.pyc', '*.pyo', '*.log',
            '*.tmp', '*.bak', '*.swp'
        ])
        self.prefix_mapping = self.config.get('prefix_mapping', {
            'icons': '/icons',
            'images': '/images',
            'styles': '/styles',
            'fonts': '/fonts',
            'translations': '/translations',
            'sounds': '/sounds',
            'data': '/data',
            'ui': '/ui'
        })
        self.custom_aliases = self.config.get('custom_aliases', {})

    def load_config(self, config_file: str) -> Dict:
        """Загружает конфигурацию из JSON файла"""
        default_config = {
            "project_root": ".",
            "output_file": "resources.qrc",
            "include_patterns": [
                "*.ico", "*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp",
                "*.svg", "*.css", "*.qss", "*.qm", "*.ttf", "*.otf",
                "*.json", "*.xml", "*.txt"
            ],
            "exclude_patterns": [
                "__pycache__", ".git", ".vscode", ".idea", "venv", "env",
                "node_modules", "dist", "build", "*.pyc", "*.pyo", "*.log",
                "*.tmp", "*.bak", "*.swp"
            ],
            "prefix_mapping": {
                "icons": "/icons",
                "images": "/images",
                "styles": "/styles",
                "fonts": "/fonts",
                "translations": "/translations",
                "sounds": "/sounds",
                "data": "/data",
                "ui": "/ui"
            },
            "custom_aliases": {
                "favicon.ico": "app_icon.ico",
                "main_style.css": "style.css"
            }
        }

        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Ошибка загрузки конфига: {e}, используем настройки по умолчанию")

        return default_config

    def save_config(self, config_file: str):
        """Сохраняет текущую конфигурацию"""
        config = {
            "project_root": str(self.project_root),
            "output_file": self.output_file,
            "include_patterns": self.include_patterns,
            "exclude_patterns": self.exclude_patterns,
            "prefix_mapping": self.prefix_mapping,
            "custom_aliases": self.custom_aliases
        }

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def is_excluded(self, path: Path) -> bool:
        """Проверяет, нужно ли исключить путь"""
        path_str = str(path)

        # Проверяем исключенные паттерны
        for pattern in self.exclude_patterns:
            if pattern.startswith('*.'):
                # Проверка по расширению
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True

        return False

    def is_included(self, path: Path) -> bool:
        """Проверяет, нужно ли включить файл"""
        if not path.is_file():
            return False

        if self.is_excluded(path):
            return False

        # Проверяем включенные паттерны
        for pattern in self.include_patterns:
            if pattern.startswith('*.'):
                if path.suffix.lower() == pattern[1:].lower():
                    return True
            elif pattern == path.name:
                return True

        return False

    def get_alias(self, file_path: Path) -> str:
        """Возвращает алиас для файла если задан"""
        filename = file_path.name
        return self.custom_aliases.get(filename, filename)

    def determine_prefix(self, file_path: Path) -> str:
        """Определяет префикс для ресурса"""
        relative_path = file_path.relative_to(self.project_root)

        # Проверяем mapping по имени папки
        for folder_name, prefix in self.prefix_mapping.items():
            if folder_name in str(relative_path.parent):
                return prefix

        # Используем имя родительской папки
        parent_name = relative_path.parent.name
        if parent_name and parent_name != '.':
            return f"/{parent_name}"

        return "/"

    def scan_project(self) -> List[Path]:
        """Сканирует проект и возвращает список файлов для включения"""
        resource_files = []

        print(f"🔍 Сканирую проект: {self.project_root}")

        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)

            # Фильтруем директории для обхода
            dirs[:] = [d for d in dirs if not self.is_excluded(root_path / d)]

            for file in files:
                file_path = root_path / file
                if self.is_included(file_path):
                    resource_files.append(file_path)

        return sorted(resource_files)

    def generate_qrc(self):
        """Генерирует .qrc файл"""
        resource_files = self.scan_project()

        if not resource_files:
            print("⚠️  Не найдено файлов для включения в ресурсы")
            return 0

        # Создаем XML структуру
        rcc = Element('RCC', version='1.0')

        # Группируем файлы по префиксам
        files_by_prefix: Dict[str, List[Path]] = {}
        for file_path in resource_files:
            prefix = self.determine_prefix(file_path)
            if prefix not in files_by_prefix:
                files_by_prefix[prefix] = []
            files_by_prefix[prefix].append(file_path)

        # Добавляем qresource для каждого префикса
        for prefix, files in sorted(files_by_prefix.items()):
            qresource = SubElement(rcc, 'qresource', prefix=prefix)
            for file_path in sorted(files):
                relative_path = file_path.relative_to(self.project_root)
                file_elem = SubElement(qresource, 'file')
                file_elem.text = str(relative_path)

                # Добавляем алиас если задан
                alias = self.get_alias(file_path)
                if alias != file_path.name:
                    file_elem.set('alias', alias)

        # Форматируем XML
        rough_string = tostring(rcc)
        tree = ElementTree(rcc)
        indent(tree, space="\t", level=0)

        # Сохраняем файл
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE RCC>\n')
        with open(self.output_file, 'ab') as f:
            ElementTree(rcc).write(f, xml_declaration=False)

        # Сохраняем конфигурацию
        self.save_config('qrc_config.json')

        # Выводим отчет
        print(f"✅ Создан файл: {self.output_file}")
        print(f"📊 Статистика:")
        print(f"   Всего файлов: {len(resource_files)}")
        print(f"   Префиксов: {len(files_by_prefix)}")

        for prefix, files in sorted(files_by_prefix.items()):
            print(f"   {prefix}: {len(files)} файлов")

        return len(resource_files)

    def create_rcc(self):
        # Проверяем наличие rcc компилятора
        try:
            # Пробуем разные имена компилятора
            compilers = ['pyrcc5', 'rcc', 'pyside2-rcc', 'pyside6-rcc']
            compiler = None

            for c in compilers:
                try:
                    subprocess.run([c, '--version'], capture_output=True, check=True)
                    compiler = c
                    print(f"Найден компилятор: {compiler}")
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue

            if not compiler:
                raise Exception("Не найден компилятор ресурсов")

            res_file = f'{os.path.splitext(self.output_file)[0]}.py'

            # Компилируем в .rcc
            cmd = [compiler, '-binary', self.output_file, '-o', res_file]
            print(f"Выполняем: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ .rcc файл успешно создан!")
                print(f"Размер: {os.path.getsize(res_file)} bytes")
            else:
                print(f"❌ Ошибка компиляции: {result.stderr}")

        except Exception as e:
            print(f"Ошибка: {e}")


def main():
    parser = argparse.ArgumentParser(description='Продвинутый генератор .qrc файлов')
    parser.add_argument('--root', default='.', help='Корневая директория проекта')
    parser.add_argument('--output', default='resources.qrc', help='Выходной .qrc файл')
    parser.add_argument('--config', default='qrc_config.json', help='Файл конфигурации')
    parser.add_argument('--init', action='store_true', help='Создать начальный конфиг')

    args = parser.parse_args()

    if args.init:
        generator = AdvancedQRCGenerator()
        generator.save_config(args.config)
        print(f"✅ Создан конфигурационный файл: {args.config}")
        return

    generator = AdvancedQRCGenerator(args.config)
    generator.project_root = Path(args.root)
    generator.output_file = args.output

    generator.generate_qrc()
    generator.create_rcc()


if __name__ == "__main__":
    """
    # Создать конфигурационный файл
    python advanced_qrc_generator.py --init
    
    # Генерировать с конфигом
    python advanced_qrc_generator.py --config my
    """

    main()
