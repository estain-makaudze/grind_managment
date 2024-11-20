const barProducts = [
    { id: 1, name: "Beer", price: 5.00, category: "Bar", image: "beer.jpg" },
    { id: 2, name: "Wine", price: 10.00, category: "Bar", image: "wine.jpg" },
    { id: 3, name: "Whiskey", price: 15.00, category: "Bar", image: "whiskey.jpg" }
];

const restaurantProducts = [
    { id: 4, name: "Burger", price: 8.00, category: "Restaurant", image: "burger.jpg" },
    { id: 5, name: "Pizza", price: 12.00, category: "Restaurant", image: "pizza.jpg" },
    { id: 6, name: "Pasta", price: 10.00, category: "Restaurant", image: "pasta.jpg" },
    { id: 4, name: "Coke", price: 1.00, category: "Restaurant", image: "burger.jpg" },
    { id: 5, name: "Coffee", price: 1.00, category: "Restaurant", image: "pizza.jpg" },
    { id: 6, name: "Water", price: 1.00, category: "Restaurant", image: "pasta.jpg" }
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

    let productName = product.name;
    let productPrice = product.price;

    // Check if product is already in cart
    const existingItem = cart.find(item => item.name === productName);
    if (existingItem) {
        existingItem.quantity += 1; // Increase quantity if item already in cart
    } else {
        cart.push({ name: productName, price: productPrice, quantity: 1 });
    }
    updateCart();
}

function updateCart() {
    cartItemsContainer.innerHTML = '';
    let total = 0;

    cart.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `${item.name} - $${item.price.toFixed(2)} x <span class="quantity-control">
            <button class="decrease-quantity"><i class="fas fa-minus"></i>-</button>
            <span class="quantity">${item.quantity}</span>
            <button class="increase-quantity"><i class="fas fa-plus"></i>+</button>
        </span>
        <button class="delete-btn">X</button>`;

        cartItemsContainer.appendChild(li);
        total += item.price * item.quantity;

        // Attach event listeners for quantity controls and delete button
        li.querySelector('.increase-quantity').addEventListener('click', function() {
            item.quantity++;
            updateCart();
        });

        li.querySelector('.decrease-quantity').addEventListener('click', function() {
            if (item.quantity > 1) {
                item.quantity--;
                updateCart();
            }
        });

        li.querySelector('.delete-btn').addEventListener('click', function() {
            cart = cart.filter(cartItem => cartItem !== item); // Remove item from cart
            updateCart();
        });
    });

    totalPriceElement.textContent = total.toFixed(2);
}

document.getElementById('checkout-btn').addEventListener('click', () => {
    if (cart.length === 0) {
        return alert('Cart is empty! Please add items to cart before checking out.');
    }

    alert(`Checkout successful! Total amount: $${totalPriceElement.textContent}`);
    cart = [];
    updateCart();
});

displayProducts(); // Initial product display for the 'Bar' category
