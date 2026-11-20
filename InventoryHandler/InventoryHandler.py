from Settings.Settings import Settings

class InventoryHandler:
    #TODO
    assets = dict_paths_to_assets #item_name - pygame.Surface
    unlockedItems = dict.fromkeys(Settings.items.Names.keys())
    unlockedKeys = dict.fromkeys(Settings.keys.Names.keys())

    @staticmethod
    def update(inventory: player.inventory) -> None:
        for item in inventory:
            Inventoryhandler.unlockedItems[item] = InventoryHandler.assets[item]

        for key in inventory:
            InventoryHandler.unlockedKeys[key] = InventoryHandler.assets[key]