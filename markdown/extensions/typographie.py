# -*- coding: utf-8 -*-

# Gestion fine de la typographie française, du moins, ce qui peut être
# automatisé, par Dominus Carnufex. Lointainement inspiré de l’extension
# SmartyPants. Licence CeCIll-B.

import markdown
from ..inlinepatterns import HtmlPattern


class RemplacerPattern(HtmlPattern):
    def __init__(self, motif, remplacement, markdown):
        """ Replacer le motif par un simple texte. """
        HtmlPattern.__init__(self, motif)
        self.remplacement = remplacement
        self.markdown = markdown

    def handleMatch(self, m):
        return self.markdown.htmlStash.store(self.remplacement, safe=True)


class TypographieExtension(markdown.extensions.Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'apostrophes': [True, 'Apostrophes typographiques'],
            'cadratins': [True, 'Tirets cadratins'],
            'demi-cadratins': [True, 'Tirets demi-cadratins'],
            'espaces': [True, 'Espaces insécables'],
            'guillemets': [True, 'Guillemets français'],
            'pour-mille': [True, 'Symbole pour mille'],
            'suspension': [True, 'Points de suspension'],
        }
        super(TypographieExtension, self).__init__(*args, **kwargs)

    def remplacerApostrophes(self, md):
        apostrophesPattern = RemplacerPattern("'", "&rsquo;", md)
        self.remplacements.add('apostrophes', apostrophesPattern, '_begin')

    def remplacerCadratins(self, md):
        cadratinsPattern = RemplacerPattern(r'(?<!-)---(?!-)', "&mdash;", md)
        self.remplacements.add('cadratins', cadratinsPattern, '_begin')

    def remplacerDemiCadratins(self, md):
        demiCadratinsPattern = RemplacerPattern(
            r'(?<!-)--(?!-)', "&ndash;", md
        )
        self.remplacements.add(
            'demi-cadratins', demiCadratinsPattern, '_begin'
        )

    def remplacerEspaces(self, md):
        espacePointVirgulePattern = RemplacerPattern(" ; ", "&nbsp;; ", md)
        espaceDeuxPointsPattern = RemplacerPattern(" : ", "&nbsp;: ", md)
        espaceInterrogationPattern = RemplacerPattern(" \?", "&nbsp;?", md)
        espaceExclamationPattern = RemplacerPattern(" !", "&nbsp;!", md)
        espacePourCentPattern = RemplacerPattern(" %", "&nbsp;%", md)
        espacePourMillePattern = RemplacerPattern(
            " ‰".decode("utf8"), "&nbsp;&permil;", md
        )
        espaceGuillemetOuvrantPattern = RemplacerPattern(
            "« ".decode("utf8"), "&laquo;&nbsp;", md
        )
        espaceGuillemetFermantPattern = RemplacerPattern(
            " »".decode("utf8"), "&nbsp;&raquo;", md
        )

        self.remplacements.add(
            'espace-point-virgule', espacePointVirgulePattern, '_end'
        )
        self.remplacements.add(
            'espace-deux-points',
            espaceDeuxPointsPattern,
            '<espace-point-virgule'
        )
        self.remplacements.add(
            'espace-interrogation',
            espaceInterrogationPattern,
            '<espace-deux-points'
        )
        self.remplacements.add(
            'espace-exclamation',
            espaceExclamationPattern,
            '<espace-interrogation'
        )
        self.remplacements.add(
            'espace-pour-cent',
            espacePourCentPattern,
            '<espace-exclamation'
        )
        self.remplacements.add(
            'espace-pour-mille',
            espacePourMillePattern,
            '<espace-pour-cent'
        )
        self.remplacements.add(
            'espace-guillemet-ouvrant',
            espaceGuillemetOuvrantPattern,
            '<espace-pour-mille'
        )
        self.remplacements.add(
            'espace-guillemet-fermant',
            espaceGuillemetFermantPattern,
            '<espace-guillemet-ouvrant'
        )

    def remplacerGuillemets(self, md):
        guillemetsOuvrantsPattern = RemplacerPattern(r'\<\<', "&laquo;", md)
        guillemetsFermantsPattern = RemplacerPattern(r'\>\>', "&raquo;", md)
        self.remplacements.add(
            'guillemets-ouvrants', guillemetsOuvrantsPattern, '_begin'
        )
        self.remplacements.add(
            'guillemets-fermants',
            guillemetsFermantsPattern,
            '>guillemets-ouvrants'
        )

    def remplacerGuillemetsEspaces(self, md):
        guillemetsOuvrantsPattern = RemplacerPattern(
            r'\<\< ', "&laquo;&nbsp;", md
        )
        guillemetsFermantsPattern = RemplacerPattern(
            r' \>\>', "&nbsp;&raquo;", md
        )
        self.remplacements.add(
            'guillemets-ouvrants', guillemetsOuvrantsPattern, '_begin'
        )
        self.remplacements.add(
            'guillemets-fermants',
            guillemetsFermantsPattern,
            '>guillemets-ouvrants'
        )

    def remplacerPourMille(self, md):
        pourMillePattern = RemplacerPattern("%o", "&permil;", md)
        self.remplacements.add('pour-mille', pourMillePattern, '_begin')

    def remplacerPourMilleEspaces(self, md):
        pourMillePattern = RemplacerPattern(" %o", "&nbsp;&permil;", md)
        self.remplacements.add('pour-mille', pourMillePattern, '_begin')

    def remplacerSuspension(self, md):
        suspensionPattern = RemplacerPattern(
            r'(?<!\.)\.{3}(?!\.)', "&hellip;", md
        )
        self.remplacements.add('suspension', suspensionPattern, '_begin')

    def extendMarkdown(self, md, md_globals):
        configs = self.getConfigs()
        self.remplacements = markdown.odict.OrderedDict()
        if configs['apostrophes']:
            self.remplacerApostrophes(md)
        if configs['cadratins']:
            self.remplacerCadratins(md)
        if configs['demi-cadratins']:
            self.remplacerDemiCadratins(md)
        if configs['espaces']:
            self.remplacerEspaces(md)
        if configs['guillemets'] and not configs['espaces']:
            self.remplacerGuillemets(md)
        if configs['guillemets'] and configs['espaces']:
            self.remplacerGuillemetsEspaces(md)
        if configs['pour-mille'] and not configs['espaces']:
            self.remplacerPourMille(md)
        if configs['pour-mille'] and configs['espaces']:
            self.remplacerPourMilleEspaces(md)
        if configs['suspension']:
            self.remplacerSuspension(md)
        traitement = markdown.treeprocessors.InlineProcessor(md)
        traitement.inlinePatterns = self.remplacements
        md.treeprocessors.add('typographie', traitement, '_end')
        md.ESCAPED_CHARS.extend(["'"])


def makeExtension(*args, **kwargs):
    return TypographieExtension(*args, **kwargs)