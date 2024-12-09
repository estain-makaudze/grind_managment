document.addEventListener("DOMContentLoaded", () => {
const modal = document.getElementById("qrModal");
const openButton = document.getElementById("checkout-btn");
const closeButton = document.querySelector(".close");
const resultDisplay = document.getElementById("receipt");
let receipt_container = document.getElementById("receipt_container");
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
                }).then(response => response.json()).then(data => {
                    console.log('response', data);
                  if (data.result.status == "ok") {

                    // setup the receipt
                    let receipt = `
                    <div class="receipt">
                        <h3>Order Receipt</h3>
                        <p>Order ID: ${orderId}</p>
                        <p>Customer ID: ${decodedText}</p>
                        <table>
                            <thead>
                                <tr>
                                    <th>Item</th>
                                    <th>Quantity</th>
                                    <th>Price</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;

                    cart.forEach(item => {
                        receipt += `
                        <tr>
                            <td>${item.name}</td>
                            <td>${item.quantity}</td>
                            <td>${item.price}</td>
                        </tr>
                        `;
                    }
                    );

                    receipt += `
                            </tbody>
                        </table>
                        <p>Total: ${totalPriceElement.textContent}</p>
                    </div>
                    `;
                    
                    receipt_container.innerHTML = receipt;
                    resultDisplay.style.display = "block";


                      // close modal
                        modal.style.display = "none";
                      alert(`Order placed successfully for ${decodedText}!`);
                      cart = [];
                      updateCart();
                  } else {
                      alert('Failed to place order');
                  }
            });

            // cart = [];
            // updateCart();
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

document.getElementById('downloadBtn').addEventListener('click', function () {
    downloadReceiptPDF(cart);
});


function downloadReceiptPDF(cart) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // setup the receipt
    let receipt = `
    Order Receipt
    Order ID: ${Date.now()}
    Customer ID: 12345
    `;
    cart.forEach(item => {
        receipt += `
        Item: ${item.name}
        Quantity: ${item.quantity}
        Price: ${item.price}
        `;
    }
    );
    receipt += `
    Total: ${totalPriceElement.textContent}
    `;

    doc.text(receipt, 10, 10);


    // Set the font size and text color
    doc.setFontSize(12);
    doc.setTextColor(100);
       

    // Save the generated PDF
    doc.save('receipt.pdf');
}
