import random
import string

def random_string(length):
    return str(''.join(random.choice(string.ascii_letters) for i in range(length)))

def remove_from_list(list, username):
    for user in list:
        if user['username'] == username:
            list.remove(user)
            return
        
def check_user(session, all_users):
    if session.get('username'):
        username = session.get('username')
        if session.get('token'):
            token = session.get('token')
            for user in all_users:
                if user['username'] == username and user['token'] == token:
                    return True
    return False

def get_user_by_username(all_users, username):
    for user in all_users:
        if user['username'] == username:
            return user
    return None

def check_server_status(rcon, RCON_PASSWORD):
    try:
        if rcon.login(RCON_PASSWORD):
            resp = rcon.command("list")
            return True
        else:
            return False
    except:
        return False
    
    
ITEM_LIST = [
    'minecraft:stone',
    'minecraft:grass',
    'minecraft:sand',
    'minecraft:gravel',
    'minecraft:dirt',
    'minecraft:cobblestone',
    'minecraft:planks',
    'minecraft:sapling',
    'minecraft:bedrock',
    'minecraft:flowing_water',
    'minecraft:water',
    'minecraft:flowing_lava',
    'minecraft:lava',
    'minecraft:sandstone',
    'minecraft:red_sandstone',
    'minecraft:gravel',
    'minecraft:gold_ore',
    'minecraft:iron_ore',
    'minecraft:coal_ore',
    'minecraft:log',
    'minecraft:leaves',
    'minecraft:sponge',
    'minecraft:glass',
    'minecraft:lapis_ore',
    'minecraft:lapis_block',
    'minecraft:dispenser',
    'minecraft:sandstone',
    'minecraft:noteblock',
    'minecraft:bed',
    'minecraft:golden_rail',
    'minecraft:detector_rail',
    'minecraft:sticky_piston',
    'minecraft:web',
    'minecraft:tallgrass',
    'minecraft:deadbush',
    'minecraft:piston',
    'minecraft:piston_head',
    'minecraft:wool',
    'minecraft:piston_extension',
    'minecraft:yellow_flower',
    'minecraft:red_flower',
    'minecraft:brown_mushroom',
    'minecraft:red_mushroom',
    'minecraft:gold_block',
    'minecraft:iron_block',
    'minecraft:double_stone_slab',
    'minecraft:stone_slab',
    'minecraft:brick_block',
    'minecraft:tnt',
    'minecraft:bookshelf',
    'minecraft:mossy_cobblestone',
    'minecraft:obsidian',
    'minecraft:torch',
    'minecraft:fire',
    'minecraft:mob_spawner',
    'minecraft:oak',
    'minecraft:spruce',
    'minecraft:birch',
    'minecraft:jungle',
    'minecraft:acacia',
    'minecraft:dark_oak',
    'minecraft:oak_stairs',
    'minecraft:cobblestone_stairs',
    'minecraft:brick_stairs',
    'minecraft:stone_brick_stairs',
    'minecraft:nether_brick_stairs',
    'minecraft:sandstone_stairs',
    'minecraft:spruce_stairs',
    'minecraft:birch_stairs',
    'minecraft:jungle_stairs',
    'minecraft:quartz_stairs',
    'minecraft:purpur_stairs',
    'minecraft:prismarine_stairs',
    'minecraft:dark_prismarine_stairs',
    'minecraft:smooth_stone',
    'minecraft:smooth_sandstone',
    'minecraft:smooth_quartz',
    'minecraft:smooth_red_sandstone',
    'minecraft:double_stone_slab2',
    'minecraft:stone_slab2',
    'minecraft:purpur_block',
    'minecraft:purpur_pillar',
    'minecraft:purpur_stairs',
    'minecraft:prismarine',
    'minecraft:prismarine_bricks',
    'minecraft:dark_prismarine',
    'minecraft:prismarine_slab',
    'minecraft:prismarine_double_slab',
    'minecraft:stained_glass',
    'minecraft:stained_glass_pane',
    'minecraft:leaves2',
    'minecraft:log2',
    'minecraft:acacia_stairs',
    'minecraft:dark_oak_stairs',
    'minecraft:slime',
    'minecraft:barrier',
    'minecraft:iron_trapdoor',
    'minecraft:prismarine_trapdoor',
    'minecraft:hay_block',
    'minecraft:carpet',
    'minecraft:hardened_clay',
    'minecraft:coal_block',
    'minecraft:packed_ice',
    'minecraft:double_plant',
    'minecraft:standing_banner',
    'minecraft:wall_banner',
    'minecraft:daylight_detector',
    'minecraft:red_sandstone',
    'minecraft:red_sandstone_stairs',
    'minecraft:double_stone_slab3',
    'minecraft:stone_slab3',
    'minecraft:spruce_fence_gate',
    'minecraft:birch_fence_gate',
    'minecraft:jungle_fence_gate',
    'minecraft:dark_oak_fence_gate',
    'minecraft:acacia_fence_gate',
    'minecraft:spruce_fence',
    'minecraft:birch_fence',
    'minecraft:jungle_fence',
    'minecraft:dark_oak_fence',
    'minecraft:acacia_fence',
    'minecraft:spruce_door',
    'minecraft:birch_door',
    'minecraft:jungle_door',
    'minecraft:acacia_door',
    'minecraft:dark_oak_door',
    'minecraft:end_rod',
    'minecraft:chorus_plant',
    'minecraft:chorus_flower',
    'minecraft:purpur_block',
    'minecraft:purpur_pillar',
    'minecraft:purpur_stairs',
    'minecraft:purpur_double_slab',
    'minecraft:purpur_slab',
    'minecraft:end_stone',
    'minecraft:beetroots',
    'minecraft:grass_path',
    'minecraft:end_gateway',
    'minecraft:repeating_command_block',
    'minecraft:chain_command_block',
    'minecraft:frosted_ice',
    'minecraft:magma',
    'minecraft:nether_wart_block',
    'minecraft:red_nether_brick',
    'minecraft:bone_block',
    'minecraft:structure_void',
    'minecraft:observer',
    'minecraft:white_shulker_box',
    'minecraft:orange_shulker_box',
    'minecraft:magenta_shulker_box',
    'minecraft:light_blue_shulker_box',
    'minecraft:yellow_shulker_box',
    'minecraft:lime_shulker_box',
    'minecraft:pink_shulker_box',
    'minecraft:gray_shulker_box',
    'minecraft:silver_shulker_box',
    'minecraft:cyan_shulker_box',
    'minecraft:purple_shulker_box',
    'minecraft:blue_shulker_box',
    'minecraft:brown_shulker_box',
    'minecraft:green_shulker_box',
    'minecraft:red_shulker_box',
    'minecraft:black_shulker_box',
    'minecraft:white_glazed_terracotta',
    'minecraft:orange_glazed_terracotta',
    'minecraft:magenta_glazed_terracotta',
    'minecraft:light_blue_glazed_terracotta',
    'minecraft:yellow_glazed_terracotta',
    'minecraft:lime_glazed_terracotta',
    'minecraft:pink_glazed_terracotta',
    'minecraft:gray_glazed_terracotta',
    'minecraft:silver_glazed_terracotta',
    'minecraft:cyan_glazed_terracotta',
    'minecraft:purple_glazed_terracotta',
    'minecraft:blue_glazed_terracotta',
    'minecraft:brown_glazed_terracotta',
    'minecraft:green_glazed_terracotta',
    'minecraft:red_glazed_terracotta',
    'minecraft:black_glazed_terracotta',
    'minecraft:concrete',
    'minecraft:concrete_powder',
    'minecraft:structure_block',
    'minecraft:iron_shovel',
    'minecraft:iron_pickaxe',
    'minecraft:iron_axe',
    'minecraft:flint_and_steel',
    'minecraft:apple',
    'minecraft:bow',
    'minecraft:arrow',
    'minecraft:coal',
    'minecraft:diamond',
    'minecraft:iron_ingot',
    'minecraft:gold_ingot',
    'minecraft:iron_sword',
    'minecraft:wooden_sword',
    'minecraft:wooden_shovel',
    'minecraft:wooden_pickaxe',
    'minecraft:wooden_axe',
    'minecraft:stone_sword',
    'minecraft:stone_shovel',
    'minecraft:stone_pickaxe',
    'minecraft:stone_axe',
    'minecraft:diamond_sword',
    'minecraft:diamond_shovel',
    'minecraft:diamond_pickaxe',
    'minecraft:diamond_axe',
    'minecraft:stick',
    'minecraft:bowl',
    'minecraft:mushroom_stew',
    'minecraft:golden_sword',
    'minecraft:golden_shovel',
    'minecraft:golden_pickaxe',
    'minecraft:golden_axe',
    'minecraft:string',
    'minecraft:feather',
    'minecraft:gunpowder',
    'minecraft:wooden_hoe',
    'minecraft:stone_hoe',
    'minecraft:iron_hoe',
    'minecraft:diamond_hoe',
    'minecraft:golden_hoe',
    'minecraft:wheat_seeds',
    'minecraft:wheat',
    'minecraft:bread',
    'minecraft:leather_helmet',
    'minecraft:leather_chestplate',
    'minecraft:leather_leggings',
    'minecraft:leather_boots',
    'minecraft:chainmail_helmet',
    'minecraft:chainmail_chestplate',
    'minecraft:chainmail_leggings',
    'minecraft:chainmail_boots',
    'minecraft:iron_helmet',
    'minecraft:iron_chestplate',
    'minecraft:iron_leggings',
    'minecraft:iron_boots',
    'minecraft:diamond_helmet',
    'minecraft:diamond_chestplate',
    'minecraft:diamond_leggings',
    'minecraft:diamond_boots',
    'minecraft:golden_helmet',
    'minecraft:golden_chestplate',
    'minecraft:golden_leggings',
    'minecraft:golden_boots',
    'minecraft:flint',
    'minecraft:porkchop',
    'minecraft:cooked_porkchop',
    'minecraft:painting',
    'minecraft:golden_apple',
    'minecraft:sign',
    'minecraft:wooden_door',
    'minecraft:bucket',
    'minecraft:water_bucket',
    'minecraft:lava_bucket',
    'minecraft:minecart',
    'minecraft:saddle',
    'minecraft:iron_door',
    'minecraft:redstone',
    'minecraft:snowball',
    'minecraft:boat',
    'minecraft:leather',
    'minecraft:milk_bucket',
    'minecraft:brick',
    'minecraft:clay_ball',
    'minecraft:reeds',
    'minecraft:paper',
    'minecraft:book',
    'minecraft:slime_ball',
    'minecraft:chest_minecart',
    'minecraft:furnace_minecart',
    'minecraft:egg',
    'minecraft:compass',
    'minecraft:fishing_rod',
    'minecraft:clock',
    'minecraft:glowstone_dust',
    'minecraft:fish',
    'minecraft:cooked_fish',
    'minecraft:dye',
    'minecraft:bone',
    'minecraft:sugar',
    'minecraft:cake',
    'minecraft:bed',
    'minecraft:repeater',
    'minecraft:cookie',
    'minecraft:filled_map',
    'minecraft:shears',
    'minecraft:melon',
    'minecraft:pumpkin_seeds',
    'minecraft:melon_seeds',
    'minecraft:beef',
    'minecraft:cooked_beef',
    'minecraft:chicken',
    'minecraft:cooked_chicken',
    'minecraft:rotten_flesh',
    'minecraft:ender_pearl',
    'minecraft:blaze',
    'minecraft:magma_cream',
    'minecraft:ghast_tear',
    'minecraft:gold_nugget',
    'minecraft:nether_wart',
    'minecraft:potion',
    'minecraft:glass_bottle',
    'minecraft:spider_eye',
    'minecraft:fermented_spider_eye',
    'minecraft:blaze_powder',
    'minecraft:magma_cream',
    'minecraft:brewing_stand',
    'minecraft:cauldron',
    'minecraft:ender_eye',
    'minecraft:speckled_melon',
    'minecraft:spawn_egg',
    'minecraft:experience_bottle',
    'minecraft:fire_charge',
    'minecraft:writable_book',
    'minecraft:written_book',
    'minecraft:emerald',
    'minecraft:item_frame',
    'minecraft:flower_pot',
    'minecraft:carrot',
    'minecraft:potato',
    'minecraft:baked_potato',
    'minecraft:poisonous_potato',
    'minecraft:map',
    'minecraft:golden_carrot',
    'minecraft:skull',
    'minecraft:carrot_on_a_stick',
    'minecraft:nether_star',
    'minecraft:pumpkin_pie',
    'minecraft:fireworks',
    'minecraft:firework_charge',
    'minecraft:enchanted_book',
    'minecraft:comparator',
    'minecraft:netherbrick',
    'minecraft:quartz',
    'minecraft:tnt_minecart',
    'minecraft:hopper_minecart',
    'minecraft:iron_horse_armor',
    'minecraft:golden_horse_armor',
    'minecraft:diamond_horse_armor',
    'minecraft:lead',
    'minecraft:name_tag',
    'minecraft:command_block_minecart',
    'minecraft:record_13',
    'minecraft:record_cat',
    'minecraft:record_blocks',
    'minecraft:record_chirp',
    'minecraft:record_far',
    'minecraft:record_mall',
    'minecraft:record_mellohi',
    'minecraft:record_stal',
    'minecraft:record_strad',
    'minecraft:record_ward',
    'minecraft:record_11',
    'minecraft:record_wait',
    'minecraft:prismarine_shard',
    'minecraft:prismarine_crystals',
    'minecraft:rabbit',
    'minecraft:cooked_rabbit',
    'minecraft:rabbit_stew',
    'minecraft:rabbit_foot',
    'minecraft:rabbit_hide',
    'minecraft:armor_stand',
    'minecraft:iron_horse_armor_head',
    'minecraft:golden_horse_armor_head',
    'minecraft:diamond_horse_armor_head',
    'minecraft:leash',
    'minecraft:name_tag',
    'minecraft:command_block_minecart',
    'minecraft:record_13',
    'minecraft:record_cat',
    'minecraft:record_blocks',
    'minecraft:record_chirp',
    'minecraft:record_far',
    'minecraft:record_mall',
    'minecraft:record_mellohi',
    'minecraft:record_stal',
    'minecraft:record_strad',
    'minecraft:record_ward',
    'minecraft:record_11',
    'minecraft:record_wait',
    'minecraft:prismarine_shard',
    'minecraft:prismarine_crystals',
    'minecraft:rabbit',
    'minecraft:cooked_rabbit',
    'minecraft:rabbit_stew',
    'minecraft:rabbit_foot',
    'minecraft:rabbit_hide',
    'minecraft:armor_stand',
    'minecraft:iron_horse_armor_head',
    'minecraft:golden_horse_armor_head',
    'minecraft:diamond_horse_armor_head',
    'minecraft:leash',
    'minecraft:name_tag',
    'minecraft:command_block_minecart',
    'minecraft:record_13',
]
        
#get random minecraft item
def random_mc_item():
    return random.choice(ITEM_LIST)