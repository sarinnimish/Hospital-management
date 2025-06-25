/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";

export class ModelListController extends ListController {
    setup() {
        super.setup();
       
    }

    onUploadClick() {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            res_model: 'button.upload',
            name: 'Upload File',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
        });
    }

    onDownloadClick() {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: 'Download File',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
        });
    }
}

registry.category("views").add("button_in_list", {
    ...listView,
    Controller: ModelListController,
    buttonTemplate: "Hospital_Management.ListView.Buttons",
});


