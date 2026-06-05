from wizard_core import Wizard
import wizard_schools
import wizard_abilities

Wizard.choose_school = wizard_schools.choose_school
Wizard.learn_spell_sort = wizard_schools.learn_spell_sort
Wizard.sort = wizard_schools.sort
Wizard.unlock_abilities = wizard_schools.unlock_abilities

Wizard.map_fire = wizard_abilities.map_fire
Wizard.reduce_ash = wizard_abilities.reduce_ash
Wizard.pyromancy_burn = wizard_abilities.pyromancy_burn
Wizard.fast_forward_time = wizard_abilities.fast_forward_time
Wizard.rewind_time = wizard_abilities.rewind_time
Wizard.freeze = wizard_abilities.freeze
Wizard.cryo_preserve = wizard_abilities.cryo_preserve
Wizard.raise_dead = wizard_abilities.raise_dead
Wizard.decay = wizard_abilities.decay
Wizard.animate = wizard_abilities.animate
Wizard.amplify = wizard_abilities.amplify
Wizard._apply_amplify = wizard_abilities._apply_amplify
Wizard.temper = wizard_abilities.temper
Wizard.surge = wizard_abilities.surge
Wizard.veil = wizard_abilities.veil
Wizard._tick_veil = wizard_abilities._tick_veil
Wizard.mimic = wizard_abilities.mimic
Wizard.shatter = wizard_abilities.shatter
Wizard.summon_elemental = wizard_abilities.summon_elemental
Wizard.conjure_supply = wizard_abilities.conjure_supply
Wizard.wild_conjure = wizard_abilities.wild_conjure
Wizard.shroud = wizard_abilities.shroud
Wizard._apply_siphon = wizard_abilities._apply_siphon
Wizard.siphon = wizard_abilities.siphon
Wizard.eclipse = wizard_abilities.eclipse
Wizard.transmute_vitae = wizard_abilities.transmute_vitae
Wizard.transmute_arcana = wizard_abilities.transmute_arcana