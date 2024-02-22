from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(length=150), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('policy_number', sa.Integer(), nullable=False),
        sa.Column('social_status', sa.String(length=100), nullable=False),
        sa.Column('medic_id', sa.Integer(), sa.ForeignKey('medics.id')),
        sa.Column('search_data', sa.JSONB(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_patients_id', 'id', unique=False, postgresql_using='gin')
    )

    op.create_table(
        'treatments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('diagnosis', sa.String(length=150), nullable=False),
        sa.Column('current_state', sa.String(length=150), nullable=False),
        sa.Column('date_start', sa.Date(), nullable=False),
        sa.Column('date_end', sa.Date(), nullable=False),
        sa.Column('patient_id', sa.Integer(), sa.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('medic_id', sa.Integer(), sa.ForeignKey('medics.id', ondelete='CASCADE'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'medics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(length=150), nullable=False),
        sa.Column('speciality', sa.String(length=100), nullable=False),
        sa.Column('exp_years', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'treatment_medic',
        sa.Column('treatment_id', sa.Integer(), sa.ForeignKey('treatments.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('medic_id', sa.Integer(), sa.ForeignKey('medics.id', ondelete='CASCADE'), primary_key=True)
    )


def downgrade():
    op.drop_table('treatment_medic')
    op.drop_table('medics')
    op.drop_table('treatments')
    op.drop_table('patients')