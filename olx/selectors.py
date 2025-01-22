class OLXSelectors:
    OLX_ID = "span.css-1i121pa::text"
    VIEWS = "span[data-testid='page-view-counter']::text"
    LISTING_GRID = "div[data-testid='listing-grid']"
    CARD = "div[data-cy='l-card']"
    LINK = "a.css-qo0cxu::attr(href)"
    TITLE = "h4.css-yde3oc::text"
    PRICE = "[data-testid='ad-price-container'] h3::text"
    PUBLISHED_AT = "span[data-cy='ad-posted-at']::text"
    DESCRIPTION = "div.css-1o924a9::text"
    TAGS = "ul.css-rn93um li::text"
    IMG_SRC = ".swiper-zoom-container img::attr(src)"

    PAGE_LANG = "normalize-space(//html/@lang)"
    ID_X = '//*[@id="mainContent"]/div/div[2]/div[3]/div[1]/div[2]/div[5]/div/span[1]/text()[2]'
    VIEWS_X = '//*[@id="mainContent"]/div/div[2]/div[3]/div[1]/div[2]/div[5]/div/span[2]/text()'
