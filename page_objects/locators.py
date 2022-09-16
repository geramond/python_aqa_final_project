from selenium.webdriver.common.by import By

BASE_PAGE_LOCATORS = {
    "logo": (By.CSS_SELECTOR, "div#logo"),
    "currency": {
        "current": (By.CSS_SELECTOR, "#form-currency button strong"),
        "dropdown": (By.CSS_SELECTOR, "#form-currency .dropdown-toggle"),
        "USD": (By.CSS_SELECTOR, ".currency-select[name='USD']"),
        "EUR": (By.CSS_SELECTOR, ".currency-select[name='EUR']"),
        "GBP": (By.CSS_SELECTOR, ".currency-select[name='GBP']"),
    },
    "header: contact us": (By.CSS_SELECTOR, "#top-links .fa-phone"),
    "header: login/register dd": (By.CSS_SELECTOR, "#top-links .fa-user"),
    "header: wish list": (By.CSS_SELECTOR, "#top-links .fa-heart"),
    "header: cart": (By.CSS_SELECTOR, "#top-links .fa-shopping-cart"),
    "header: share": (By.CSS_SELECTOR, "#top-links .fa-share"),
    "navbar": (By.CSS_SELECTOR, ".navbar#menu"),
    "navbar items": (By.CSS_SELECTOR, "ul.navbar-nav>li"),
    "cart button": (By.CSS_SELECTOR, "#cart>button"),
    "search input": (By.CSS_SELECTOR, "#search>input"),
    "search button": (By.CSS_SELECTOR, "#search button"),
}

ADD_PRODUCT_PAGE_LOCATORS = {
    "first name": (By.CSS_SELECTOR, "#input-firstname"),
    "last name": (By.CSS_SELECTOR, "#input-lastname"),
    "email": (By.CSS_SELECTOR, "#input-email"),
    "telephone": (By.CSS_SELECTOR, "#input-telephone"),
    "password": (By.CSS_SELECTOR, "#input-password"),
    "password confirm": (By.CSS_SELECTOR, "#input-confirm"),
    "newsletter: yes": (By.CSS_SELECTOR, "[name=newsletter][value=1]"),
    "newsletter: no": (By.CSS_SELECTOR, "[name=newsletter][value=0]"),
    "agree to privacy policy checkbox": (By.CSS_SELECTOR, "[name=agree]"),
    "continue": (By.CSS_SELECTOR, "[value=Continue]"),
    "success message title": (By.CSS_SELECTOR, "#content h1"),
    "error banner": (By.CSS_SELECTOR, ".alert-danger"),
    "login link": (By.CSS_SELECTOR, "#content>p>a"),
}

ADMIN_PAGE_LOCATORS = {
    # Dashboard page locators
    "open catalog": (By.CSS_SELECTOR, "#menu-catalog>a"),
    "catalog: products": (By.LINK_TEXT, "Products"),

    # Login page locators
    "username": (By.CSS_SELECTOR, "#input-username"),
    "password": (By.CSS_SELECTOR, "#input-password"),
    "login button": (By.CSS_SELECTOR, "[type=submit]"),
    "forgotten password": (By.CSS_SELECTOR, ".help-block a"),
    "logo": (By.CSS_SELECTOR, "#header-logo a"),
    "page title": (By.CSS_SELECTOR, "h1"),
    "error banner": (By.CSS_SELECTOR, ".alert-danger"),
    "close error banner button": (By.CSS_SELECTOR, "button.close"),
    "email": (By.CSS_SELECTOR, "#input-email"),

    # Product page locators
    "add new": (By.CSS_SELECTOR, 'a[data-original-title="Add New"]'),
    "delete": (By.CSS_SELECTOR, 'button[data-original-title="Delete"]'),
    "filter: name": (By.CSS_SELECTOR, '#input-name'),
    "filter: model": (By.CSS_SELECTOR, '#input-model'),
    "filter": (By.CSS_SELECTOR, '#button-filter'),
    "products on page": (By.CSS_SELECTOR, 'td input'),
}

CATALOG_PAGE_LOCATORS = {
    "catalog page title": (By.CSS_SELECTOR, "h2"),
    "products on page": (By.CSS_SELECTOR, ".product-layout"),
    "products on page list": (By.CSS_SELECTOR, ".product-layout.product-list"),
    "products on page grid": (By.CSS_SELECTOR, ".product-layout.product-grid"),
    "no products in category": (By.CSS_SELECTOR, "div#content>p"),
    "no products in category > continue button": (By.CSS_SELECTOR, ".buttons .pull-right"),
    "grid view button": (By.CSS_SELECTOR, "#grid-view"),
    "list view button": (By.CSS_SELECTOR, "#list-view"),
    "add to cart buttons": (By.CSS_SELECTOR, ".button-group .fa-shopping-cart"),
    "add to wish list buttons": (By.CSS_SELECTOR, ".button-group .fa-heart"),
    "add to comparison buttons": (By.CSS_SELECTOR, ".button-group .fa-exchange"),
    "alert": (By.CSS_SELECTOR, "div.alert"),
}

MAIN_PAGE_LOCATORS = {
    "featured: add to cart buttons": (By.CSS_SELECTOR, ".button-group .fa-shopping-cart"),
    "featured: add to wish list buttons": (By.CSS_SELECTOR, ".button-group .fa-heart"),
    "featured: add to comparison buttons": (By.CSS_SELECTOR, ".button-group .fa-exchange"),
    "alert": (By.CSS_SELECTOR, "div.alert"),
}

PRODUCT_PAGE_LOCATORS = {
    "product name": (By.CSS_SELECTOR, "h1"),
    "product name in breadcrumb navigation": (By.CSS_SELECTOR, "ul.breadcrumb li:last-child"),
    "product description": (By.CSS_SELECTOR, "div#tab-description"),
    "product price": (By.CSS_SELECTOR, "li h2"),
    "product main image": (By.CSS_SELECTOR, "#content li:not(.image-additional) .thumbnail"),
    "product additional images": (By.CSS_SELECTOR, "#content .image-additional"),
    "add to cart required fields": (By.CSS_SELECTOR, "#product .form-group.required"),
    "add to wish list": (By.CSS_SELECTOR, ".btn-group .fa-heart"),
    "add to comparison": (By.CSS_SELECTOR, ".btn-group .fa-exchange"),
}

REGISTER_PAGE_LOCATORS = {
    "first name": (By.CSS_SELECTOR, "#input-firstname"),
    "last name": (By.CSS_SELECTOR, "#input-lastname"),
    "email": (By.CSS_SELECTOR, "#input-email"),
    "telephone": (By.CSS_SELECTOR, "#input-telephone"),
    "password": (By.CSS_SELECTOR, "#input-password"),
    "password confirm": (By.CSS_SELECTOR, "#input-confirm"),
    "newsletter: yes": (By.CSS_SELECTOR, "[name=newsletter][value=1]"),
    "newsletter: no": (By.CSS_SELECTOR, "[name=newsletter][value=0]"),
    "agree to privacy policy checkbox": (By.CSS_SELECTOR, "[name=agree]"),
    "continue": (By.CSS_SELECTOR, "[value=Continue]"),
    "success message title": (By.CSS_SELECTOR, "#content h1"),
    "error banner": (By.CSS_SELECTOR, ".alert-danger"),
    "login link": (By.CSS_SELECTOR, "#content>p>a"),
}

ADD_PRODUCT_PAGE_LOCATORS = {
    "save": (By.CSS_SELECTOR, 'button[data-original-title="Save"]'),
    "general": {
        "name": (By.CSS_SELECTOR, '#input-name1'),
        "description": (By.CSS_SELECTOR, 'div.note-editable'),
        "meta": (By.CSS_SELECTOR, '#input-meta-title1'),
        "meta description": (By.CSS_SELECTOR, '#input-meta-description1'),
        "meta keywords": (By.CSS_SELECTOR, '#input-meta-keyword1'),
        "product tags": (By.CSS_SELECTOR, '#input-tag1'),
    },
    "tab": {
        "general": (By.LINK_TEXT, 'General'),
        "data": (By.LINK_TEXT, 'Data'),
        "links": (By.LINK_TEXT, 'Links'),
        "attribute": (By.LINK_TEXT, 'Attribute'),
        "option": (By.LINK_TEXT, 'Option'),
        "recurring": (By.LINK_TEXT, 'Recurring'),
        "discount": (By.LINK_TEXT, 'Discount'),
        "special": (By.LINK_TEXT, 'Discount'),
        "image": (By.LINK_TEXT, 'Image')
    },
    "data": {
        "model": (By.CSS_SELECTOR, '#input-model')
    },
    "error banner": (By.CSS_SELECTOR, '.alert-danger'),
    "page title": (By.CSS_SELECTOR, 'h3.panel-title'),
}
