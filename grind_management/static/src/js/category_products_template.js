/** @odoo-module **/
import { Component } from '@odoo/owl';

export class TempView extends Component {
    static template = 'grind_management.TempViewTemplate';
    setup() {
        // State management to determine which section to show
        this.state = useState({
            showProducts: true,  // Default view
        });
    }

    toggleView(view) {
        // Toggle based on button clicked
        if (view === 'products') {
            this.state.showProducts = true;
        } else if (view === 'menus') {
            this.state.showProducts = false;
        }
    }
}
