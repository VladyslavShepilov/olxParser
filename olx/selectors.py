class OLXSelectors:
    LISTING_GRID = "div[data-testid='listing-grid']"
    CARD = "div[data-cy='l-card']"
    LINK = 'a.css-qo0cxu::attr(href)'
    ID = "span.css-12hdxwj::text"
    VIEWS = "span.page-view-counter::text"
    TITLE = "h4.css-1kc83jo::text"
    PRICE = "h3.css-90xrc0::text"
    PUBLISHED_AT = "span[data-cy='ad-posted-at']::text"
    DESCRIPTION = "div.css-1o924a9::text"
    TAGS = "ul.css-rn93um p.css-b5m1rv span::text, ul.css-rn93um p.css-b5m1rv::text"
    IMG_SRC = ".swiper-zoom-container img::attr(src)"
