let currentCategory = 'Inventory'; // Default category
let cart = [];

const productContainer = document.getElementById('products');
const cartItemsContainer = document.getElementById('cart-items');
const totalPriceElement = document.getElementById('total-price');
const totalQuantityElement = document.getElementById('total-quantity');

// Fetch products dynamically
async function fetchProducts() {
    const response = await fetch('/grind_shop_products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });

    if (response.ok) {
        const data = await response.json(); // Use .json() instead of .text()
        return data;
    } else {
        console.error('Failed to fetch products');
        return null;
    }
}

// Display products based on the selected category
async function displayProducts() {
    const data = await fetchProducts();

    if (!data) {
        productContainer.innerHTML = '<p>Error loading products</p>';
        return;
    }

    const products = currentCategory === 'Inventory' ? data.inventory_products : data.menu_ingredients;
    productContainer.innerHTML = '';

    products.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product');
        productDiv.innerHTML = `
             <div class="col">
              <div class="card bg-light shadow-sm h-100">
                <div class="card-body d-flex flex-column justify-content-between">
                  <div class="text-end">
                    <h5 class="card-title mb-1">${product.name}</h5>
                  </div>
                  <p t-if='currentCategory == 'Inventory'' class="card-text text-start mb-1 small">Available Quantity: ${product.available_quantity}</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="badge bg-secondary fst-italic">Price: $${product.price.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>
        `;

        productDiv.addEventListener('click', () => addToCart(product));
        productContainer.appendChild(productDiv);
    });
}

document.getElementById('inventory-btn').addEventListener('click', () => {
    currentCategory = 'Inventory';
    displayProducts();
});

// click a link with class inventory-btn click event
let inventory_btn = document.getElementById('inventory-btn');
inventory_btn.click();

document.getElementById('menu-btn').addEventListener('click', () => {
    currentCategory = 'Menu';
    displayProducts();
});

// Rest of the cart functionality remains the same
function addToCart(product) {
    console.log('Adding to cart:', product);
    const existingItem = cart.find(item => item.name === product.name);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ name: product.name, price: product.price, quantity: 1 });
    }
    updateCart();
}

function updateCart() {
    cartItemsContainer.innerHTML = '';
    let total = 0;
    let total_quantity = 0;

    cart.forEach(item => {
        const cart_div = document.createElement('div');
        cart_div.innerHTML = `
            <div class="card w-100 mt-3">
              <div class="card-body">
                <h5 class="card-title">${item.name}</h5>
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <p class="card-text mb-0">Qty: ${item.quantity} $${item.price.toFixed(2)}</p>
                  </div>
                  <div class="d-flex gap-2">
                    <button class="delete-btn btn btn-sm btn-outline-danger">Delete</button>
                    <button class="increase-quantity btn btn-sm btn-outline-success">+1</button>
                    <button class="decrease-quantity btn btn-sm btn-outline-secondary">-1</button>
                  </div>
                </div>
              </div>
            </div>`;

        cartItemsContainer.appendChild(cart_div);
        total += item.price * item.quantity;
        total_quantity += item.quantity;

        cart_div.querySelector('.increase-quantity').addEventListener('click', () => {
            item.quantity++;
            updateCart();
        });

        cart_div.querySelector('.decrease-quantity').addEventListener('click', () => {
            if (item.quantity > 1) {
                item.quantity--;
                updateCart();
            }
        });

        cart_div.querySelector('.delete-btn').addEventListener('click', () => {
            cart = cart.filter(cartItem => cartItem !== item);
            updateCart();
        });
    });

    totalPriceElement.textContent = total.toFixed(2);
    totalQuantityElement.textContent = total_quantity;
}

document.getElementById('clear-cart-btn').addEventListener('click', () => {
    console.log('Clearing cart');
    cart = [];
    updateCart();
});

displayProducts(); // Initial display
