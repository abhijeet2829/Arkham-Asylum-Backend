from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from arkham_app.models import CellBlock, InmateProfile, MedicalFile
import random

class Command(BaseCommand):
    help = 'Seeds the Arkham Asylum database with 10 records per model'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Initiating secure Arkham database seeding protocol...'))

        groups_data = ['Super Admin', 'Medical Staff', 'Security Staff', 'Public Visitor']
        groups = {}
        for g_name in groups_data:
            group, created = Group.objects.get_or_create(name=g_name)
            groups[g_name] = group
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Group: {g_name}'))

        inmate_ct = ContentType.objects.get_for_model(InmateProfile)
        medical_ct = ContentType.objects.get_for_model(MedicalFile)
        
        medic_perms = Permission.objects.filter(content_type__in=[inmate_ct, medical_ct], codename__in=['view_inmateprofile', 'view_medicalfile', 'change_medicalfile'])
        groups['Medical Staff'].permissions.set(medic_perms)
        
        guard_perms = Permission.objects.filter(content_type=inmate_ct, codename__in=['view_inmateprofile', 'change_inmateprofile'])
        groups['Security Staff'].permissions.set(guard_perms)

        public_perms = Permission.objects.filter(content_type=inmate_ct, codename__in=['view_inmateprofile'])
        groups['Public Visitor'].permissions.set(public_perms)

        blocks_data = [
            {'name': 'Block-A Maximum', 'capacity': 5},
            {'name': 'Block-B Solitary', 'capacity': 3},
            {'name': 'Block-C Transitional', 'capacity': 10},
        ]
        db_blocks = []
        for b in blocks_data:
            block, created = CellBlock.objects.get_or_create(name=b['name'], defaults={'max_capacity': b['capacity']})
            db_blocks.append(block)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Secured Cell Block: {block.name}'))

        users_data = [
            ("bruce", "batman", "Super Admin"),
            ("Warden", "DN09r;naCtj", "Super Admin"),
            ("ArkhamDirector", "Gh0tham!Ctrl9", "Super Admin"),
            ("Leland", "cS4QzQWU'OC", "Medical Staff"),
            ("DrThompkins", "RxCrim3$Ally", "Medical Staff"),
            ("DrElliot", "Hush!M3nd92", "Medical Staff"),
            ("NurseQuinn", "H4rl3y!Psych", "Medical Staff"),
            ("MedTechFries", "Cry0g3n!cLab", "Medical Staff"),
            ("DrDundee", "N1ghtSh!ft07", "Medical Staff"),
            ("KaneHarrel", "U4d;'U05nK0", "Security Staff"),
            ("CashAaron", "B10ckC!Duty5", "Security Staff"),
            ("BulletBoles", "Tr4nsf3r!K9", "Security Staff"),
            ("NorthEddie", "W4tch!Tow3r1", "Security Staff"),
            ("BryanDouglas", "G4teK33p!ng", "Security Staff"),
            ("SgtHarvey", "P4trol!Rng08", "Security Staff"),
            ("JohnDoe", "dcIXcw',btF", "Public Visitor"),
            ("ValeVicki", "Pr3ss!P4ss01", "Public Visitor"),
            ("JackRyder", "M3dia!B4dge7", "Public Visitor"),
            ("SummerGleeson", "N3ws!D3sk42", "Public Visitor"),
            ("ArtBrown", "V1sit0r!Day6", "Public Visitor"),
            ("MikeEngel", "GCN!L1veF33d", "Public Visitor")
        ]
        
        doctors = []
        for username, password, role in users_data:
            user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@arkham.com'})
            if created:
                user.set_password(password)
                if role == "Super Admin":
                    user.is_superuser = True
                    user.is_staff = True
                user.save()
            user.groups.add(groups[role])
            if role == 'Medical Staff':
                doctors.append(user)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Registered Personnel: {username} ({role})'))

        inmates_data = [
            ("The Joker", "Red Hood", "Psychosis and violent nihilism"),
            ("Harvey Dent", "Two-Face", "Dissociative Identity Disorder"),
            ("Pamela Isley", "Poison Ivy", "Ecoterrorism obsession, botanical toxicity"),
            ("Victor Fries", "Mr. Freeze", "Cryogenic dependency, severe depression"),
            ("Jonathan Crane", "Scarecrow", "Phobophobia, hallucinogen addiction"),
            ("Edward Nygma", "The Riddler", "Narcissistic Personality Disorder, OCD"),
            ("Oswald Cobblepot", "The Penguin", "Megalomaniacal hoarding"),
            ("Waylon Jones", "Killer Croc", "Epidermolytic hyperkeratosis, cannibalism"),
            ("Jervis Tetch", "Mad Hatter", "Schizophrenia, obsessive linguistic fixation"),
            ("Basil Karlo", "Clayface", "Severe body dysmorphia")
        ]

        for name, alias, diagnosis in inmates_data:
            block = random.choice(db_blocks)
            
            if not InmateProfile.objects.filter(name=name).exists():
                if block.current_count < block.max_capacity:
                    inmate = InmateProfile.objects.create(name=name, alias=alias, cell_block=block, status='ACTIVE')
                    
                    doc = random.choice(doctors)
                    MedicalFile.objects.create(
                        inmate=inmate,
                        referral_diagnosis=diagnosis,
                        internal_diagnosis="Baseline established.",
                        meds="Standard sedatives",
                        assigned_to=doc
                    )
                    self.stdout.write(self.style.SUCCESS(f'Admitted Patient: {name} [{alias}] to {block.name}. File assigned to Doctor {doc.username}.'))
                else:
                    self.stdout.write(self.style.ERROR(f'Capacity Breach: Could not admit {name} to {block.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Patient {name} already exists in registry.'))

        self.stdout.write(self.style.SUCCESS('Database seeding protocol complete. 10 Entities successfully ingested.'))