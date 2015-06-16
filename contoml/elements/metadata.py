
from .common import *
from contoml import tokens
from contoml.elements import InvalidElementError


class WhitespaceElement(TokenElement):
    """
    An element that contains tokens of whitespace
    """

    def __init__(self, _tokens):
        TokenElement.__init__(self, _tokens, TYPE_METADATA)
    
    def _validate_tokens(self, _tokens):
        for token in _tokens:
            if token.type != tokens.TYPE_WHITESPACE:
                raise InvalidElementError('Tokens making up a WhitespaceElement must all be whitespace')


class NewlineElement(TokenElement):
    """
    An element containing newline tokens

    Raises:
        InvalidElementError: when passed an invalid sequence of tokens.
    """

    def __init__(self, _tokens):
        TokenElement.__init__(self, _tokens, TYPE_METADATA)

    def _validate_tokens(self, _tokens):
        for token in _tokens:
            if token.type != tokens.TYPE_NEWLINE:
                raise InvalidElementError('Tokens making a NewlineElement must all be newlines')


class CommentElement(TokenElement):
    """
    An element containing a single comment token followed by a newline token

    Raises:
        InvalidElementError: when passed an invalid sequence of tokens.
    """

    def __init__(self, _tokens):
        TokenElement.__init__(self, _tokens, TYPE_METADATA)

    def _validate_tokens(self, _tokens):
        if len(_tokens) != 2 or _tokens[0].type != tokens.TYPE_COMMENT or _tokens[1].type != tokens.TYPE_NEWLINE:
            raise InvalidElementError('CommentElement needs exactly one comment token followed by a newline token')


class PunctuationElement(TokenElement):
    """
    An element containing a single punctuation token.

    Raises:
        InvalidElementError: when passed an invalid sequence of tokens.
    """

    def __init__(self, _tokens):
        TokenElement.__init__(self, _tokens, TYPE_METADATA)

    @property
    def token(self):
        """
        Returns the token contained in this Element.
        """
        return self.tokens[0]

    def _validate_tokens(self, _tokens):
        if not _tokens or not tokens.is_operator(_tokens[0]):
            raise InvalidElementError('PunctuationElement must be made of only a single operator token')
