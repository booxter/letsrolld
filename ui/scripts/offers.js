import { important_offers } from "/scripts/variables.js";

export default class Offers {
    constructor(offers) {
        this.offers = this.getOffersLogoes(offers);
    }

    getOffersLogoes(offers) {
        offers.map((offer) => {
            important_offers.includes(offer.name) ? offer.logo = `../img/offers_icons/svg/${offer.name}.svg` : offer.logo = null;
        });
        return offers;
    }
    
    getAllOffers() {
        return this.offers;
    }


    filterImportant() {
        return this.offers.filter(o => o.logo !== null);
    }
}