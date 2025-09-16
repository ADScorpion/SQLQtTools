from SqlQtTools.qt.core import QFile, QIcon, QPixmap, QSize



class ResourceManager:
    @staticmethod
    def get_icon(icon_path, size: QSize = QSize(16, 16)):
        """Получение иконки из ресурсов"""
        icon = QIcon(f":{icon_path}")
        icon.actualSize(size)
        return icon

    @staticmethod
    def get_pixmap(self, image_path):
        """Получение изображения из ресурсов"""
        return QPixmap(f":{image_path}")

    @staticmethod
    def read_file(self, file_path):
        """Чтение файла из ресурсов"""
        try:
            file = QFile(f":{file_path}")
            if file.open(QFile.ReadOnly | QFile.Text):
                content = file.readAll().data().decode('utf-8')
                file.close()
                return content
        except:
            pass

        # Fallback: чтение из файловой системы
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""

    # TODO этот метод нужно переделать
    # def _svg_to_icon(self, key, svg_data: str, size: QSize = QSize(16, 16)) -> QIcon:
    #     if key not in self._cache_icon:
    #         if key not in self._cache_pixmap:
    #             svg_data = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size.width().real}" height="{size.height().real}" fill="currentColor" viewBox="0 0 {size.width().real} {size.height().real}">{svg_data}</svg>"""
    #             svg_bytes = QByteArray(svg_data.encode('utf-8'))
    #             renderer = QSvgRenderer(svg_bytes)
    #             pixmap = QPixmap(size)
    #             pixmap.fill(Qt.GlobalColor.transparent)
    #             painter = QPainter(pixmap)
    #             renderer.render(painter)
    #             painter.end()
    #             self._cache_pixmap[key] = pixmap
    #         self._cache_icon[key] = QIcon(self._cache_pixmap[key])
    #     return self._cache_icon[key]
