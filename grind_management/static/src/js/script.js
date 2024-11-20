
// RPC call to get all products here
const barProducts = [
    { id: 1, name: "Beer", price: 5.00, category: "Bar", image: "beer.jpg" },
    { id: 2, name: "Wine", price: 10.00, category: "Bar", image: "wine.jpg" },
    { id: 3, name: "Whiskey", price: 15.00, category: "Bar", image: "whiskey.jpg" }
];

const restaurantProducts = [
    { id: 4, name: "Burger", price: 8.00, category: "Restaurant", image: "burger.jpg" },
    { id: 5, name: "Pizza", price: 12.00, category: "Restaurant", image: "pizza.jpg" },
    { id: 6, name: "Pasta", price: 10.00, category: "Restaurant", image: "pasta.jpg" }
];

let currentCategory = 'Bar';
let cart = [];

const productContainer = document.getElementById('products');
const cartItemsContainer = document.getElementById('cart-items');
const totalPriceElement = document.getElementById('total-price');

document.getElementById('bar-btn').addEventListener('click', () => {
    currentCategory = 'Bar';
    displayProducts();
});

document.getElementById('restaurant-btn').addEventListener('click', () => {
    currentCategory = 'Restaurant';
    displayProducts();
});

function displayProducts() {
    const products = currentCategory === 'Bar' ? barProducts : restaurantProducts;
    productContainer.innerHTML = '';

    products.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product');
        productDiv.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <h4>${product.name}</h4>
            <p>$${product.price.toFixed(2)}</p>
        `;
        productDiv.addEventListener('click', () => addToCart(product));
        productContainer.appendChild(productDiv);
    });
}

function addToCart(product) {
    cart.push(product);
    updateCart();
}

function updateCart() {
    cartItemsContainer.innerHTML = '';
    let total = 0;

    cart.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - $${item.price.toFixed(2)}`;
        cartItemsContainer.appendChild(li);
        total += item.price;
    });

    totalPriceElement.textContent = total.toFixed(2);
}

document.getElementById('checkout-btn').addEventListener('click', () => {
    alert(`Checkout successful! Total amount: $${totalPriceElement.textContent}`);
    cart = [];
    updateCart();
});

displayProducts(); // Initial product display for the 'Bar' category
