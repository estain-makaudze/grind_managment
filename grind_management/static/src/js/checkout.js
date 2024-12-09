document.addEventListener("DOMContentLoaded", () => {
const modal = document.getElementById("qrModal");
const openButton = document.getElementById("checkout-btn");
const closeButton = document.querySelector(".close");
const resultDisplay = document.getElementById("qr-result");
const qrReaderContainer = document.getElementById("qr-reader");
let html5QrCode;

    // Open modal
    openButton.onclick = () => {
        console.log('Open modal');
        if (cart.length === 0) {
            return alert('Cart is empty! Please add items to cart before checking out.');
        }
        modal.style.display = "block";

        // Initialize QR Code Scanner
        html5QrCode = new Html5Qrcode("qr-reader");
        html5QrCode.start(
            { facingMode: "environment" }, // Use back camera
            {
                fps: 10, // Frames per second
                qrbox: { width: 500, height: 500 }
            },
            (decodedText) => {
                // Handle the scanned QR code
                // resultDisplay.textContent = `Scanned Code: ${decodedText}`;

                const orderId = Date.now();
                let order = { "params" : {
                    "orderId": orderId,
                    "cart": cart,
                    "total": parseFloat(totalPriceElement.textContent),
                    "user_id": decodedText
                    }
                }

                fetch('/checkout', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                    },
                  body: JSON.stringify(order),
                }).then(response => {
                  if (response.ok) {
                      // close modal
                        modal.style.display = "none";
                      alert(`Order placed successfully for ${decodedText}!`);
                      cart = [];
                      updateCart();
                  } else {
                      alert('Failed to place order');
                  }
            });

            cart = [];
            updateCart();
                html5QrCode.stop(); // Stop scanner
            },
            (errorMessage) => {
                console.log(`QR Code Scan Error: ${errorMessage}`);
            }
        ).catch((err) => {
            console.error(`Error starting QR code scanner: ${err}`);
        });
    };

    // Close modal
    closeButton.onclick = () => {
        modal.style.display = "none";
        if (html5QrCode) {
            html5QrCode.stop().then(() => {
                html5QrCode.clear();
            });
        }
    };

    // Close modal when clicking outside
    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
            if (html5QrCode) {
                html5QrCode.stop().then(() => {
                    html5QrCode.clear();
                });
            }
        }
    };
});
